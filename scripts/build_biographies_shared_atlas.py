#!/usr/bin/env python3
"""Deterministic research navigation; --check is read-only. No publication approval."""
import argparse
import hashlib
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
GRAPH = Path('data/biographies-shared-atlas-v1.json')
OUTPUT = Path('БИОГРАФИИ/atlas')
TYPES = {'TEACHER', 'ACQUAINTANCE', 'EDITORIAL_COMPARISON', 'EDITORIAL_CLAIM',
         'RECEPTION', 'DOCTRINAL_TEXT', 'CONTEXT', 'NAVIGATION'}
AXES = ('evidenceClass', 'accessState', 'locatorState', 'rightsState', 'publicationState', 'holds')
COLORS = {'NAVIGATION': '#64748b', 'CONTEXT': '#b45309', 'TEACHER': '#0369a1',
          'ACQUAINTANCE': '#0369a1', 'RECEPTION': '#7c3aed', 'DOCTRINAL_TEXT': '#047857',
          'EDITORIAL_COMPARISON': '#be185d', 'EDITORIAL_CLAIM': '#be185d'}


def load(root=ROOT):
    graph = json.loads((root / GRAPH).read_text())
    registry = json.loads((root / graph['anchorRegistry']).read_text())
    return graph, registry


def validate(graph, registry, root=ROOT):
    if graph.get('authorityRole') != 'supporting-navigation-only':
        raise ValueError('Atlas must not claim root or publication authority')
    ids = set()
    for node in graph['nodes']:
        if node['id'] in ids:
            raise ValueError('Duplicate node')
        ids.add(node['id'])
        target = (root / node['owner']).resolve()
        if not target.is_relative_to(root.resolve()) or not target.is_file():
            raise ValueError('Missing or unsafe owner: ' + node['owner'])
        for coord in ['x', 'y']:
            if not isinstance(node[coord], int) or not 0 <= node[coord] <= 1300:
                raise ValueError('Invalid layout coordinate')
    anchors = registry['anchors'] + registry['supportAnchors']
    by_id = {a['id']: a for a in anchors}
    if len(by_id) != len(anchors):
        raise ValueError('Duplicate anchor ID')
    edge_ids = set()
    for edge in graph['edges']:
        if edge['id'] in edge_ids:
            raise ValueError('Duplicate edge')
        edge_ids.add(edge['id'])
        if edge['from'] not in ids or edge['to'] not in ids or edge['type'] not in TYPES:
            raise ValueError('Unknown node or edge type')
        if not edge.get('boundary'):
            raise ValueError('Missing claim boundary')
        if edge['type'] != 'NAVIGATION' and not edge['refs']:
            raise ValueError('Historical edge without evidence')
        if edge['type'] == 'NAVIGATION' and edge['refs']:
            raise ValueError('Navigation must not masquerade as evidence')
        for ref in edge['refs']:
            if ref not in by_id:
                raise ValueError('Unknown anchor: ' + ref)
            a = by_id[ref]
            if any(k not in a for k in AXES):
                raise ValueError('Missing state axis')
            if a['evidenceClass'] not in {'A1', 'A2', 'A3', 'B1', 'C', 'D'}:
                raise ValueError('Unknown evidence class')
            if a['evidenceClass'] in {'C', 'D'} or a['locatorState'] != 'EXACT_LOCATOR_VERIFIED':
                raise ValueError('Unsupported evidence for visible historical edge')
            if 'PUBLICATION_HOLD' not in a['holds']:
                raise ValueError('Atlas requires explicit research/publication boundary')
            sources = registry['sources'] if a in registry['anchors'] else registry['supportSources']
            if a['source'] not in sources:
                raise ValueError('Unknown source')
    for edge in graph['excludedLinks']:
        if edge['id'] in edge_ids or edge['status'] not in {'SUPERSEDED', 'EXCLUDED', 'CONFLICT'}:
            raise ValueError('Excluded edge leaked or invalid status')
        if edge['from'] not in ids or edge['to'] not in ids or not edge['reason']:
            raise ValueError('Malformed exclusion')
        if any(ref not in by_id for ref in edge['refs']):
            raise ValueError('Unknown exclusion anchor')
    return by_id


def href(owner):
    return '../../' + quote(owner, safe='/')


def esc(text):
    return html.escape(str(text), quote=True)


def render(graph, registry, root=ROOT):
    anchors = validate(graph, registry, root)
    fingerprint = hashlib.sha256(json.dumps([graph, registry], ensure_ascii=False,
                                            sort_keys=True).encode()).hexdigest()
    nodes = {n['id']: n for n in graph['nodes']}
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 980" role="img" aria-labelledby="title desc">',
           '<title id="title">Биографии и богословские вопросы — общий исследовательский атлас</title>',
           '<desc id="desc">Стрелка обозначает подписанный тип связи, не общее влияние. Серый пунктир — только навигация; оранжевый — фон. Все связи остаются исследовательскими.</desc>',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker></defs>',
           '<rect width="1400" height="980" fill="#f8fafc"/>',
           '<text x="60" y="42" font-family="sans-serif" font-size="25" fill="#0f172a">Общий атлас: люди · тексты · темы · отделы</text>',
           '<text x="60" y="70" font-family="sans-serif" font-size="16" fill="#475569">Исследовательская навигация — не доказательство влияния и не разрешение публикации</text>']
    for edge in graph['edges']:
        a, b = nodes[edge['from']], nodes[edge['to']]
        x1, y1, x2, y2 = a['x']+180, a['y']+36, b['x']+180, b['y']+36
        # Clip endpoints to the card border. Curves do not encode time or causation.
        if x1 != x2:
            x1 += 180 if x2 > x1 else -180
            x2 += -180 if x2 > x1 else 180
        else:
            y1 += 36 if y2 > y1 else -36
            y2 += -36 if y2 > y1 else 36
        color = COLORS[edge['type']]
        dash = ' stroke-dasharray="7 7"' if edge['type'] in {'CONTEXT', 'NAVIGATION', 'EDITORIAL_COMPARISON'} else ''
        title = edge['id'] + ' · ' + edge['type'] + ': ' + edge['label'] + '. ' + edge['boundary']
        out.append(f'<path data-type="{edge["type"]}" d="M{x1} {y1} C{(x1+x2)//2} {y1},{(x1+x2)//2} {y2},{x2} {y2}" fill="none" stroke="{color}" stroke-width="2"{dash} marker-end="url(#arrow)"><title>{esc(title)}</title></path>')
    for n in graph['nodes']:
        out.append(f'<a href="{href(n["owner"])}"><title>{esc(n["owner"])}</title><rect x="{n["x"]}" y="{n["y"]}" width="360" height="72" rx="10" fill="white" stroke="#94a3b8"/><text x="{n["x"]+14}" y="{n["y"]+28}" font-family="sans-serif" font-size="17" fill="#0f172a">{esc(n["label"])}</text><text x="{n["x"]+14}" y="{n["y"]+53}" font-family="sans-serif" font-size="13" fill="#64748b">{esc(n["kind"])} · открыть владельца</text></a>')
    out.append('</svg>')
    svg = '\n'.join(out) + '\n'
    cards = []
    for e in graph['edges']:
        citations = []
        for ref in e['refs']:
            a = anchors[ref]
            sources = registry['sources'] if a in registry['anchors'] else registry['supportSources']
            source = sources[a['source']]
            loc = a.get('locator') or ('TEI pp. ' + ', '.join(str(x) if x else 'без номера' for x in a['teiPages']))
            state = ' / '.join(str(a[k]) for k in AXES[:-1]) + ' / ' + ', '.join(a['holds'])
            citations.append(f'<li><strong>{esc(ref)}</strong> · <a href="{esc(source["url"])}">{esc(a["source"])}</a> · {esc(loc)}<p>{esc(a["claimBoundary"])}</p><small>{esc(state)}</small></li>')
        if not citations:
            citations = ['<li>Навигация без доказательственного класса. Исторический вывод не заявлен.</li>']
        cards.append(f'<article data-type="{e["type"]}" id="{esc(e["id"])}"><h3>{esc(nodes[e["from"]]["label"])} → {esc(nodes[e["to"]]["label"])}</h3><b>{esc(e["type"])} · {esc(e["label"])}</b><p>{esc(e["boundary"])}</p><ul>{"".join(citations)}</ul></article>')
    excluded = ''.join(f'<li><b>{esc(e["id"])} · {esc(e["status"])}</b>: {esc(e["reason"])}</li>' for e in graph['excludedLinks'])
    opts = ''.join(f'<option>{typ}</option>' for typ in sorted(TYPES))
    document = f'''<!doctype html>
<html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Общий исследовательский атлас биографий</title>
<style>body{{font:17px/1.6 system-ui,sans-serif;color:#172033;max-width:1440px;margin:auto;padding:24px;background:#f8fafc}}a{{color:#075985}}svg{{width:100%;min-width:850px;height:auto}}.diagram{{overflow:auto;border:1px solid #cbd5e1;border-radius:12px}}article{{background:white;padding:20px;margin:16px 0;border:1px solid #cbd5e1;border-radius:12px}}small{{overflow-wrap:anywhere;color:#475569}}select{{font:inherit;padding:8px}}[hidden]{{display:none!important}}</style>
<h1>Люди, тексты и богословские вопросы</h1>
<p>{esc(graph['scope'])}</p>
<p><strong>Серый пунктир — навигация, оранжевый — фон, синий — личная связь по названному свидетелю, розовый — редакционное действие, фиолетовый — рецепция, зелёный — доктринальный текст.</strong> Положение узлов не кодирует хронологию. Стрелка не означает общее влияние. Подробные ограничения и пять осей — в карточках ниже.</p>
<p>Начальный слой: {len(graph['nodes'])} узлов, {len(graph['edges'])} связей. Это выборка, не инвентаризация всех людей и источников. Исторические связи и навигационные маршруты считаются отдельно.</p>
<label>Показать тип связи: <select id="filter"><option value="all">Все</option>{opts}</select></label>
<div class="diagram">{svg}</div>
<h2>Проверяемые связи и пределы</h2>{''.join(cards)}
<h2>Исключённые связи — не нарисованы</h2><ul>{excluded}</ul>
<h2>Владельцы и воспроизводимость</h2>
<p><a href="{href(str(GRAPH))}">Реестр карты</a> · <a href="{href(graph['anchorRegistry'])}">Реестр доказательств</a> · <a href="{href('БИОГРАФИИ/Стивен Чарнок/07_REPO_CROSSLINKS_AND_DRIVE_MIRROR.md')}">Ранее собранные употребления</a> · <a href="{href('БИОГРАФИИ/00_README_AND_NAVIGATION.md')}">Отдел биографий</a> · <a href="biographies-shared.svg">Отдельный SVG</a></p>
<p>Проекция наследует классы и HOLD источников, не повышает их. Ручной веб-слой не становится автоматически проверенным XML. Product publication / deployed status не заявлены.</p>
<small>SHA256 нормализованных входных JSON: {fingerprint}</small>
<script>document.getElementById('filter').addEventListener('change',function(){{for(const el of document.querySelectorAll('[data-type]')){{el.toggleAttribute('hidden',this.value!=='all'&&el.dataset.type!==this.value);}}}});</script></html>
'''
    return {'biographies-shared.svg': svg, 'index.html': document}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validate and compare generated bytes, without writing')
    args = parser.parse_args()
    graph, registry = load()
    for name, content in render(graph, registry).items():
        p = ROOT / OUTPUT / name
        if args.check:
            if not p.exists() or p.read_bytes() != content.encode():
                raise SystemExit('STALE: ' + str(p))
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(content.encode())
    print('Shared biographies atlas: PASS' + (' (read-only check)' if args.check else ' (generated)'))


if __name__ == '__main__':
    main()

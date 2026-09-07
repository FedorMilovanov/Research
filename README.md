# Research

Исследовательский backend и база знаний для доказательной работы по материалам проекта `gb-is-my-strength` и связанным корпусам.

## Читать сначала

1. [`CURRENT_AUTHORITY.md`](CURRENT_AUTHORITY.md) — стабильная точка входа в текущую межкорпусную authority.
2. [`AGENT_RULES.md`](AGENT_RULES.md) — обязательные правила агентов.
3. [`data/research-authority-registry-v1.json`](data/research-authority-registry-v1.json) — машинный SSOT корневой authority и её зависимостей.
4. [`data/repository-evidence-policy-v2.json`](data/repository-evidence-policy-v2.json) — каноническая evidence-policy.
5. [`00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md`](00_RESEARCH_CONTROL_PLANE_AUTHORITY_2026-08-02.md) — control-plane authority.

Нельзя выбирать «самый свежий по имени» датированный `00_RESEARCH_CURRENT_AUTHORITY_*.md`. Корневой current owner определяется только machine registry и проверяемым stable entrypoint.

## Evidence model

Глобальные классы источников: `A1`, `A2`, `A3`, `B1`, `C`, `D`. `HOLD` не является классом источника. Независимо фиксируются:

- `evidenceClass`;
- `accessState`;
- `locatorState`;
- `rightsState`;
- `publicationState`;
- типизированные HOLD-флаги.

Research presence, Drive presence, URL reachability и bibliographic record сами по себе не доказывают соответственно publication approval, rights, content verification или наличие полного объекта.

## Связь с Product

Публичный продукт: [FedorMilovanov/gb-is-my-strength](https://github.com/FedorMilovanov/gb-is-my-strength).

`Research closure != Product write != publication approval != deployed/live evidence`.

Перенос в Product требует явного claim/source handoff и отдельной Product-проверки на текущем source anchor.

## Основные текущие corpus entrypoints

- Бытие 6 / Иуда / 1–2 Петра: [`ТРУДНЫЕ ТЕКСТЫ/00_GENESIS6_MASTER_AUTHORITY_INDEX_AND_SUPERSESSION_MAP_XLII.md`](%D0%A2%D0%A0%D0%A3%D0%94%D0%9D%D0%AB%D0%95%20%D0%A2%D0%95%D0%9A%D0%A1%D0%A2%D0%AB/00_GENESIS6_MASTER_AUTHORITY_INDEX_AND_SUPERSESSION_MAP_XLII.md).
- «Серия Сердце»: [`СЕРИЯ СЕРДЦЕ/00_CURRENT_AUTHORITY_2026-08-02.md`](%D0%A1%D0%95%D0%A0%D0%98%D0%AF%20%D0%A1%D0%95%D0%A0%D0%94%D0%A6%D0%95/00_CURRENT_AUTHORITY_2026-08-02.md).
- Библейский атлас: [`БИБЛЕЙСКИЙ АТЛАС/00_CURRENT_AUTHORITY_2026-08-02.md`](%D0%91%D0%98%D0%91%D0%9B%D0%95%D0%99%D0%A1%D0%9A%D0%98%D0%99%20%D0%90%D0%A2%D0%9B%D0%90%D0%A1/00_CURRENT_AUTHORITY_2026-08-02.md).
- Баптистские архивы: [`RUSSIAN_BAPTISTS_ARCHIVE/SCAN_ACQUISITION_CURRENT_AUTHORITY_2026-08-02.md`](RUSSIAN_BAPTISTS_ARCHIVE/SCAN_ACQUISITION_CURRENT_AUTHORITY_2026-08-02.md).
- Джон Гилл: [`Джон Гилл/75_CLOSED_BOOK_FAMILY_ACQUISITION_AUTHORITY_2026-08-02.md`](%D0%94%D0%B6%D0%BE%D0%BD%20%D0%93%D0%B8%D0%BB%D0%BB/75_CLOSED_BOOK_FAMILY_ACQUISITION_AUTHORITY_2026-08-02.md).
- Source Library: [`SOURCE_LIBRARY/CURRENT_SOURCE_URL_AUTHORITY_2026-08-02.md`](SOURCE_LIBRARY/CURRENT_SOURCE_URL_AUTHORITY_2026-08-02.md).

Corpus-specific current authority остаётся владельцем своего evidence graph. Корневой registry определяет навигацию и stage boundary, но не переписывает corpus-specific evidence.

## Историческая навигация

Предыдущий большой README сохранён без потерь как [`history/README_CORPUS_INDEX_2026-08-17.md`](history/README_CORPUS_INDEX_2026-08-17.md). Это dated snapshot навигации и provenance; его внутренние слова «текущая authority» не переопределяют `CURRENT_AUTHORITY.md` или machine registry.

## Проверка

```bash
python3 scripts/validate_research_root_authority.py
```

Validator read-only и fail-closed: проверяет единственный root owner, существование transitive authority paths и отсутствие прямых dated-root ссылок в operational entrypoints.

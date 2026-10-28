#!/usr/bin/env python3
"""Build the copy-ready HTML page for the hymnsforgod post, and check it.

Telegram does not parse Markdown on paste: a text written as ``**жирный**``
arrives in the channel with the asterisks showing. The post therefore has to
exist in three shapes at once —

  1. Telegram markup (``**``/``*``) — what the .md file carries and what is
     pasted into a field that does render it;
  2. HTML (``<b>``/``<i>``) — what Telegram Desktop 6.8.0+ takes from the
     clipboard (changelog, 07.05.26: "Copy and paste formatting to and from
     HTML") and what a bot takes with ``parse_mode=HTML``;
  3. clean text — what lands in a client that understands neither.

Three hand-kept copies of one hymn is how a line drifts. This script derives
shapes 2 and 3 from shape 1, compares them with what the .md already states,
refuses to write the page if they disagree, and emits the page itself.

It also enforces the Bot API rule that every ``<``, ``>`` and ``&`` outside a
tag must be escaped — the 1676 print of the Dutch original carries
``Voyse: Un jour &c.``, and an unescaped ``&`` there is a rejection, not a
rendering.

Read-only except for the page it writes. Usage:
    python3 SUNO_HYMNS/scripts/render_telegram_html.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SUNO = ROOT / "SUNO_HYMNS" / "SUNO"
MD = SUNO / "DUTCH-005_TELEGRAM_HYMNSFORGOD.md"
PAGE = SUNO / "DUTCH-005_TELEGRAM_HYMNSFORGOD.html"

TG_LIMIT = 4096


def fenced(src: str, lang: str) -> list[str]:
    return re.findall(rf"```{lang}\n(.*?)\n```", src, re.S)


def markup_to_html(text: str) -> str:
    """Telegram markup -> Bot API HTML. Wrappers never cross a line break."""
    out = html.escape(text, quote=False)
    out = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"\*(.+?)\*", r"<i>\1</i>", out)
    return out


def visible(text: str) -> str:
    return text.replace("*", "")


def unescape(text: str) -> str:
    return html.unescape(text)


CARD = """
      <section class="card">
        <div class="card-head">
          <h2>{label}</h2>
          <span class="count">{count} знаков из {limit}</span>
        </div>
        <div class="preview" id="preview-{index}">{html}</div>
        <div class="buttons">
          <button type="button" onclick="copyRich({index}, this)">Скопировать с разметкой</button>
          <button type="button" class="ghost" onclick="copyBot({index}, this)">Скопировать HTML для бота</button>
          <button type="button" class="ghost" onclick="copyMarkup({index}, this)">Скопировать разметку Telegram</button>
          <button type="button" class="ghost" onclick="selectText({index}, this)">Выделить</button>
        </div>
      </section>
"""


def build_page(messages: list[dict]) -> str:
    cards = "".join(
        CARD.format(
            index=index,
            label=message["label"],
            count=message["count"],
            limit=message["limit"],
            html=message["html"],
        )
        for index, message in enumerate(messages)
    )
    payload = json.dumps({"messages": messages}, ensure_ascii=False).replace("</", "<\\/")
    page = PAGE_TEMPLATE.replace("__CARDS__", cards).replace("__DATA__", payload)
    return page


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DUTCH-005 — пост для t.me/hymnsforgod (копия с разметкой)</title>
<style>
  :root { color-scheme: light; }
  body {
    margin: 0; padding: 32px 20px 64px;
    font: 15px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: #f6f4f0; color: #1b1b1b;
  }
  main { max-width: 860px; margin: 0 auto; }
  h1 { font-size: 22px; margin: 0 0 4px; }
  .sub { color: #6b6b6b; margin: 0 0 24px; }
  .status {
    border-left: 3px solid #b4552d; background: #fff6ef;
    padding: 12px 16px; margin: 0 0 24px; border-radius: 0 6px 6px 0;
  }
  .status p { margin: 0 0 6px; }
  .status p:last-child { margin-bottom: 0; }
  .how { background: #fff; border: 1px solid #e2ddd5; border-radius: 8px; padding: 16px 20px; margin: 0 0 28px; }
  .how ol { margin: 8px 0 0; padding-left: 22px; }
  .how li { margin-bottom: 10px; }
  .how li:last-child { margin-bottom: 0; }
  .card { background: #fff; border: 1px solid #e2ddd5; border-radius: 8px; padding: 18px 20px; margin: 0 0 22px; }
  .card-head { display: flex; align-items: baseline; justify-content: space-between; gap: 16px; flex-wrap: wrap; }
  .card-head h2 { font-size: 17px; margin: 0 0 12px; }
  .count { color: #6b6b6b; font-size: 13px; }
  .preview {
    white-space: pre-wrap; word-wrap: break-word;
    font: 16px/1.62 Georgia, "Iowan Old Style", "Times New Roman", serif;
    background: #fbfaf8; border: 1px solid #ece7df; border-radius: 6px;
    padding: 16px; margin: 0 0 14px; max-height: 420px; overflow: auto;
  }
  .buttons { display: flex; flex-wrap: wrap; gap: 8px; }
  button {
    font: 14px/1 inherit; padding: 9px 14px; border-radius: 6px; cursor: pointer;
    border: 1px solid #1b1b1b; background: #1b1b1b; color: #fff;
  }
  button.ghost { background: #fff; color: #1b1b1b; border-color: #cfc9c0; }
  button.ghost:hover { border-color: #1b1b1b; }
  button.ok { background: #1f7a3d; border-color: #1f7a3d; color: #fff; }
  button.bad { background: #b4552d; border-color: #b4552d; color: #fff; }
  footer { color: #6b6b6b; font-size: 13px; border-top: 1px solid #e2ddd5; padding-top: 16px; }
  a { color: #1b1b1b; }
  code { font-size: 13px; background: #efece6; padding: 1px 4px; border-radius: 3px; }
</style>
</head>
<body>
<main>
  <h1>DUTCH-005 «Хвала Славе» — пост для канала t.me/hymnsforgod</h1>
  <p class="sub">Два сообщения. Разметка уже внутри: копируйте и вставляйте, asterisks в текст не попадут.</p>

  <div class="status">
    <p><strong>Не опубликовано.</strong> Ревизия <code>DUTCH-005-RU v0.10</code> — рабочий черновик:
      заголовок утверждён, wording владельцем <strong>не подписан</strong>. Строка III.2
      «Та, что за смертью придёт» применена по прочтению и подписи не имеет.
      Публиковать — только после подписи.</p>
    <p><strong>Это адаптация, а не перевод.</strong> Так и сказано в посте. Ни строки, ни припева,
      ни повтора не прибавлено.</p>
    <p><strong>Ссылок в посте нет</strong> и добавлять нельзя: для hymnsforgod в репозитории нет
      ни сайта, ни плейлиста, ни VK. Футер из <code>projects/lord-god-strength</code> сюда не переносится —
      это другой канал.</p>
  </div>

  <div class="how">
    <strong>Как вставить, чтобы жирный и курсив доехали</strong>
    <ol>
      <li><strong>Telegram Desktop 6.8.0 и новее</strong> (выпуск 7 мая 2026; в changelog прямо
        сказано: «Copy and paste formatting to and from HTML»; текущая версия — 7.3.3).
        Нажмите <em>«Скопировать с разметкой»</em> под сообщением, затем Ctrl+V в поле ввода канала.
        Разметка приезжает вместе с текстом.</li>
      <li><strong>Через бота</strong> — работает и с телефона, где буфер обмена форматирование не держит.
        Нажмите <em>«Скопировать HTML для бота»</em> и отправьте вызовом
        <code>sendMessage</code> с <code>parse_mode=HTML</code>. Текст подготовлен именно для этого
        режима: <code>&lt;</code>, <code>&gt;</code> и <code>&amp;</code> вне тегов заменены на сущности,
        как требует Bot API.</li>
      <li><strong>Если браузер не дал доступ к буферу</strong> (например, страница открыта внутри
        чужого окна): <em>«Выделить»</em>, затем Ctrl+C самостоятельно. Браузер кладёт в буфер и
        разметку, и простой текст — Telegram Desktop возьмёт разметку.</li>
    </ol>
    <p style="margin:12px 0 0">Вставляйте долгим нажатием → «Вставить» из системного меню.
      Вставка из буфера клавиатуры форматирование снимает.</p>
  </div>

__CARDS__

  <footer>
    Страница собрана скриптом <code>SUNO_HYMNS/scripts/render_telegram_html.py</code> из
    <code>DUTCH-005_TELEGRAM_HYMNSFORGOD.md</code>: три формы текста (разметка Telegram, HTML,
    чистый текст) выводятся из одного источника и сверяются между собой. Ни одна строка не
    набрана вручную. Лимит одного сообщения — 4096 знаков; счётчики над карточками —
    по видимому тексту, без символов разметки.
  </footer>
</main>

<script type="application/json" id="post-data">__DATA__</script>
<script>
var DATA = JSON.parse(document.getElementById('post-data').textContent);

function flash(btn, text, ok) {
  if (!btn.dataset.label) btn.dataset.label = btn.textContent;
  btn.textContent = text;
  btn.classList.add(ok ? 'ok' : 'bad');
  setTimeout(function () {
    btn.textContent = btn.dataset.label;
    btn.classList.remove('ok', 'bad');
  }, 2400);
}

function selectNode(node) {
  var range = document.createRange();
  range.selectNodeContents(node);
  var sel = window.getSelection();
  sel.removeAllRanges();
  sel.addRange(range);
}

function copyFromDom(node) {
  var holder = document.createElement('div');
  holder.setAttribute('contenteditable', 'true');
  holder.style.position = 'fixed';
  holder.style.left = '-9999px';
  holder.style.whiteSpace = 'pre-wrap';
  holder.innerHTML = node.innerHTML;
  document.body.appendChild(holder);
  selectNode(holder);
  var ok = false;
  try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  window.getSelection().removeAllRanges();
  document.body.removeChild(holder);
  return ok;
}

function copyPlain(text) {
  var ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.left = '-9999px';
  document.body.appendChild(ta);
  ta.select();
  var ok = false;
  try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
  document.body.removeChild(ta);
  return ok;
}

function writePlain(text, btn, label) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(text).then(
      function () { flash(btn, label, true); },
      function () { flash(btn, copyPlain(text) ? label : 'Не дали доступ — выделите и Ctrl+C', copyPlain(text)); }
    );
    return;
  }
  var ok = copyPlain(text);
  flash(btn, ok ? label : 'Не дали доступ — выделите и Ctrl+C', ok);
}

function giveUp(btn) {
  flash(btn, 'Теперь нажмите Ctrl+C', false);
}

function copyRich(i, btn) {
  var m = DATA.messages[i];
  var node = document.getElementById('preview-' + i);
  if (navigator.clipboard && window.ClipboardItem) {
    var item = new ClipboardItem({
      'text/html': new Blob([m.html], { type: 'text/html' }),
      'text/plain': new Blob([m.plain], { type: 'text/plain' })
    });
    navigator.clipboard.write([item]).then(
      function () { flash(btn, 'Скопировано с разметкой', true); },
      function () { if (copyFromDom(node)) { flash(btn, 'Скопировано с разметкой', true); } else { selectNode(node); giveUp(btn); } }
    );
    return;
  }
  if (copyFromDom(node)) { flash(btn, 'Скопировано с разметкой', true); }
  else { selectNode(node); giveUp(btn); }
}

function copyBot(i, btn) { writePlain(DATA.messages[i].html, btn, 'HTML скопирован'); }

function copyMarkup(i, btn) { writePlain(DATA.messages[i].markdown, btn, 'Разметка скопирована'); }

function selectText(i, btn) {
  selectNode(document.getElementById('preview-' + i));
  flash(btn, 'Выделено — Ctrl+C', true);
}
</script>
</body>
</html>
"""


def main() -> int:
    problems: list[str] = []
    src = MD.read_text(encoding="utf-8")
    texts, stored_html = fenced(src, "text"), fenced(src, "html")

    if len(texts) != 2 or len(stored_html) != 2:
        print(f"FAIL: expected 2 text blocks and 2 html blocks, found {len(texts)} and {len(stored_html)}")
        return 1

    messages: list[dict] = []
    for index, (text, stored) in enumerate(zip(texts, stored_html), 1):
        label = f"Сообщение {index}"
        generated = markup_to_html(text)
        # compare the words, not the escaping: an unescaped & in the file is a
        # defect to report, not a difference in content
        if unescape(stored) != unescape(generated):
            for n, (a, b) in enumerate(zip(unescape(stored).split("\n"), unescape(generated).split("\n")), 1):
                if a != b:
                    problems.append(f"{label}: строка {n} расходится с разметкой:\n  файл: {a!r}\n  из разметки: {b!r}")
            if not problems:
                problems.append(f"{label}: HTML-блок не совпадает с разметкой Telegram")
            continue
        if "&amp;" not in stored and "&" in stored:
            problems.append(
                f"{label}: символ & не заменён на &amp; — с parse_mode=HTML бот такое не примет"
            )
        if not (len(stored.split("\n")) == len(generated.split("\n"))):
            problems.append(f"{label}: число строк в HTML-блоке и в разметке разное")

        plain = visible(text)
        count = len(plain)
        stated = re.search(rf"Сообщение {index}[^\n]*?(\d+)\*{{0,2}} знаков", src)
        print(f"{label}: {count} видимых знаков, строк {len(text.splitlines())}")
        if stated is None:
            problems.append(f"{label}: в .md не указана длина")
        elif int(stated.group(1)) != count:
            problems.append(f"{label}: в .md указано {stated.group(1)} знаков, по факту {count}")
        if count > TG_LIMIT:
            problems.append(f"{label}: {count} знаков, лимит {TG_LIMIT}")

        messages.append(
            {
                "label": label,
                "count": count,
                "limit": TG_LIMIT,
                "html": generated,
                "plain": plain,
                "markdown": text,
            }
        )

    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        return 1

    PAGE.write_text(build_page(messages), encoding="utf-8")
    print(f"written: {PAGE.relative_to(ROOT)} ({PAGE.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

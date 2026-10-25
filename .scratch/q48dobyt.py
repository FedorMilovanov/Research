# -*- coding: utf-8 -*-
"""Круг 48, починка счётчика «Добыть:»:mechanical счётчик назван mechanically, баланс переснят итерацией."""
import pathlib, re

P = pathlib.Path("/home/user/Research/docs/research/atonement/35_four_point_authors_mass_registry.md")
t = P.read_text(encoding="utf-8")

OLD_TAIL = ("«Добыть:» остаётся 2 — REQ-7 (принадлежность цитат переводу Уинертона) и REQ-8 (Cunningham, "
            "pp. 333–370, закрытый доступ HathiTrust).")
NEW_TAIL = ("Счётчик `grep -c 'Добыть:'` даёт 4 строки: одна — строка таблицы `FP-162`, три — prose-упоминания "
            "токена, включая это. Висящих нужд при этом две: REQ-7 (принадлежность цитат переводу Уинертона) и REQ-8 "
            "(Cunningham, pp. 333–370, закрытый доступ HathiTrust). С круга 48 поле `dobytLines` в реестре корпуса "
            "значит именно механический счётчик строк, а не число нужд, и расхождение названо словами, а не "
            "сглажено числом.")
assert t.count(OLD_TAIL) == 1
t = t.replace(OLD_TAIL, NEW_TAIL, 1)
OLD_BAL = "`Добыть:` — 2. Числа сняты после дописки"
NEW_BAL = "`Добыть:` — 4 строки по механическому счётчику (было 2) при двух висящих нуждах (REQ-7, REQ-8). Числа сняты после дописки"
assert t.count(OLD_BAL) == 1
t = t.replace(OLD_BAL, NEW_BAL, 1)
# снятие ложного «prose»-англицизма
t = t.replace("три — prose-упоминания токена", "три — упоминания токена в прозе", 1)

def counts(txt):
    b = len(txt.encode())
    l = len(txt.rstrip("\n").split("\n"))
    return b, l

mo = list(re.finditer(r"^\*\*Баланс круга:\*\*[^\n]*$", t, re.M))[-1]
bal = mo.group(0)
base = t[: mo.start()]
for it in range(40):
    cand = base + bal + "\n"
    b, l = counts(cand)
    sp = lambda x: f"{x:,}".replace(",", " ")
    new = bal
    m = re.search(r"занимает (\d[\d ]*) байт и (\d[\d ]*) строк", bal)
    new = bal[: m.start(1)] + sp(b) + bal[m.end(1): m.start(2)] + sp(l) + bal[m.end(2):]
    if new == bal:
        break
    bal = new
else:
    raise SystemExit("баланс не сошёлся")
t = base + bal + "\n"
b, l = counts(t)
assert ("занимает %s байт и %s строк" % (f"{b:,}".replace(",", " "), f"{l:,}".replace(",", " "))) in t
rows = len([x for x in t.split("\n") if re.match(r"^\| FP-\d+ \|", x)])
cls = {}
for ln in [x for x in t.split("\n") if re.match(r"^\| FP-\d+ \|", x)]:
    k = re.findall(r"`(A1|A2|B1|B2|C)`", ln)[0]
    cls[k] = cls.get(k, 0) + 1
q = len(set(re.findall(r"^- Q-(\d+) —", t, re.M)))
assert (rows, q, cls["A1"], cls["C"]) == (209, 97, 37, 97), (rows, q, cls)
P.write_text(t, encoding="utf-8")
print("OK registry: байт %d строк %d рядов %d классы %s очередь %d" % (b, l, rows, cls, q))

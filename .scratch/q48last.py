# -*- coding: utf-8 -*-
"""Круг 48, последняя правка до зеркалирования: сноска к старому счётчику в §43 и смягчение причинного утверждения в 17_.(1)."""
import pathlib, re

REG = pathlib.Path("/home/user/Research/docs/research/atonement/35_four_point_authors_mass_registry.md")
REC = pathlib.Path("/home/user/Research/ИСКУПЛЕНИЕ/17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md")

# 1) реестр: оговорка к предложению круга 42 о счётчике
t = REG.read_text(encoding="utf-8")
OLD = "`grep -c 'Добыть:'` после этого равен 2 (был 1), и это правильный счётчик: он мерит висящие нужды"
NEW = ("`grep -c 'Добыть:'` после этого равен 2 (был 1), и тогда это был правильный счётчик: он мерил висящие нужды "
       "(круг 48 показывает предел меры: тот же `grep -c` даёт 4 строки при 2 нуждах, потому что токен стоит и в прозе, "
       "— счётчик переназван в §47)")
assert t.count(OLD) == 1, t.count(OLD)
t = t.replace(OLD, NEW, 1)

mo = list(re.finditer(r"^\*\*Баланс круга:\*\*[^\n]*$", t, re.M))[-1]
bal = mo.group(0)
base = t[: mo.start()]
sp = lambda x: f"{x:,}".replace(",", " ")
for _ in range(40):
    cand = base + bal + "\n"
    b = len(cand.encode())
    l = len(cand.rstrip("\n").split("\n"))
    m = re.search(r"занимает (\d[\d ]*) байт и (\d[\d ]*) строк", bal)
    new = bal[: m.start(1)] + sp(b) + bal[m.end(1): m.start(2)] + sp(l) + bal[m.end(2):]
    if new == bal:
        break
    bal = new
else:
    raise SystemExit("баланс не сошёлся")
t = base + bal + "\n"
b = len(t.encode())
l = len(t.rstrip("\n").split("\n"))
assert ("занимает %s байт и %s строк" % (sp(b), sp(l))) in t
assert len([x for x in t.split("\n") if re.match(r"^\| FP-\d+ \|", x)]) == 209
REG.write_text(t, encoding="utf-8")
print("реестр:", b, l, "Добыть-строк:", len([x for x in t.split("\n") if "Добыть:" in x]))

# 2) 17_: причинное утверждение снимается
s = REC.read_text(encoding="utf-8")
O = "Q-74 — в *The Rambler* Сэмюэла Джонсона за год 1752."
N = ("Q-74 — в *The Rambler* Сэмюэла Джонсона: между адресом и книгой только совпадение по году 1752, и большая "
     "причина подмены документально не установлена.")
assert s.count(O) == 1, s.count(O)
s = s.replace(O, N, 1)
REC.write_text(s, encoding="utf-8")
print("17_:", len(s.encode()), len(s.rstrip("\n").split("\n")))

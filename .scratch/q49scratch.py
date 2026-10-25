# -*- coding: utf-8 -*-
"""Круг 49: абзац о том, куда девать оцифровки, + пересъём баланса + числа лага в JSON и индексе."""
import pathlib, re, json, hashlib, datetime
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
REG = pathlib.Path("/home/user/Research/docs/research/atonement/35_four_point_authors_mass_registry.md")
t = REG.read_text(encoding="utf-8")
ANCH = "**Числа, названные с масштабом.**"
i = t.index(ANCH)
NEWP = """**Про то, где лежат оцифровки.** Круг прочитал четыре TEI-файла и таблицу переписи (в рабочем дереве это
`.scratch/`, 29 МБ только таблицы), и ни один из них в реестр не перенесён: переносить нечего, потому что правило 25
сверит байты файла реестра с именем слепка на Drive, а раздувание реестра чужими корпусами сделало бы переливку
тяжелее каждого следующего круга. Файлы, попавшие в индекс дерева коммитом круга до этой правки, из индекса сняты тем
же кругом (содержимое на месте, в песочнице), и это записано здесь, а не в молчании: круг обязан называть, что он
оставил в истории, а что — только в рабочем дереве.

"""
t = t[:i] + NEWP + t[i:]
BAL = re.compile(r"\*\*Баланс круга:\*\*[^\n]*(?=\n)")
NEW_BAL = ("**Баланс круга:** файл реестра после правки занимает @@B@@ байт и @@L@@ строк (было 469 418 байт и 1 447 "
 "строк); строки-носители позиции 209; классы `A1` 38 (+1), `A2` 35, `B1` 34, `B2` 6, `C` 96 (−1) — третий сдвиг "
 "классов подряд, и первый с круга 21, где строка поднята по тому, где номер страницы набран римской цифрой на recto "
 "и перезапускается по отделам; очередь 96 адресов (было 97: снят Q-24); доля очереди, закрытой тем, что уже лежит в "
 "лане, — 6 из 102, то есть 5.88 %, остаток 94.12 %; доля `A1` — 18.18 % от 209, и оба определения доли "
 "(целочисленное деление и округление правила 23) впервые с круга 47 дают одно число — 18; строк с механической "
 "пометкой о добыче — @@D@@ (счётчик мерит по строке и считает сам себя, поэтому его и не пересчитываю вслепую: "
 "реальных нужд по-прежнему две — REQ-7 и REQ-8). Числа сняты после дописки этого предложения и сходятся итерацией.")
sp = lambda x: f"{x:,}".replace(",", " ")
def measure(txt):
    return (len(txt.encode()), len(txt.rstrip("\n").split("\n")), len([x for x in txt.split("\n") if "Добыть:" in x]))
for n in range(80):
    b, l, dd = measure(t)
    bal = NEW_BAL.replace("@@B@@", sp(b)).replace("@@L@@", sp(l)).replace("@@D@@", str(dd))
    m = list(BAL.finditer(t))[-1]
    t2 = t[:m.start()] + bal + t[m.end():]
    if t2 == t:
        break
    t = t2
else:
    raise SystemExit("баланс не сошёлся")
rows = [x for x in t.split("\n") if re.match(r"^\| FP-\d+ \|", x)]
cls = {}
for ln in rows:
    head = re.match(r"^\| FP-\d+ \|[^|]*\|[^|]*\|[^|]*\|[^|]*\|", ln).group(0)
    cls[re.findall(r"`(A1|A2|B1|B2|C)`", head)[0]] = cls.get(re.findall(r"`(A1|A2|B1|B2|C)`", head)[0], 0) + 1
q = len(set(re.findall(r"^- Q-(\d+) —", t, re.M)))
b, l, dd = measure(t)
assert (len(rows), q, cls, dd) == (209, 96, {"A1": 38, "A2": 35, "B1": 34, "B2": 6, "C": 96}, 4), (len(rows), q, cls, dd)
md5 = hashlib.md5(t.encode()).hexdigest()
sha = hashlib.sha256(t.encode()).hexdigest()
REG.write_text(t, encoding="utf-8")
print("реестр: байт %d строк %d md5 %s" % (b, l, md5))

# --- обновить числа лага в корпусе и в индексе ---
COR = pathlib.Path("/home/user/Research/ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
J = json.loads(COR.read_text(encoding="utf-8"))
R = J["fourPointMassRegistry20261023"]
R["fileBytesAsOfRound49"] = b
R["fileMd5AsOfRound49"] = md5
R["fileSha256AsOfRound49"] = sha
R["linesAsOfRound49"] = l
R["registrySectionsMeasured"]["lines"] = l
R["registrySectionsMeasured"]["reshotBy"] = ("круг 49 (2026-10-25): H2 стал %d, потому что добавлен раздел ## 48; H3 "
 "не двинулся (%d) — круг писал прозой без новых подразделов; %d строк и %d байт пересняты тем же обходом, каким "
 "сведён баланс круга" % (R["registrySectionsMeasured"]["H2"], R["registrySectionsMeasured"]["H3"], l, b))
dm = J["driveMirrors"]["massRegistry20261023"]
dm["lagBehindGit"] = ("слепок #37 = состояние круга 48 (469418 B, md5 f4a7f749a1717271d0a6c69d7f95def1, 1447 строк, "
 "209 строк-носителей); в дереве после круга 49 лежит файл в %d B, md5 %s, %d строк при тех же 209 строках-носителях; "
 "расхождение объявлено здесь и закрывается в этом же круге переливкой 38-го слепка (см. pour38_20261025r49) с "
 "переименованием #37 в УСТАРЕЛО" % (b, md5, l))
dm["lagDeclared20261025r49"]["байтДерево"] = b
dm["lagDeclared20261025r49"]["строкиДерево"] = l
dm["fileLines"] = l
dm["how"] = ("тридцать девятая переливка готовится: реестр правился до зеркала (%d B / %d строк / md5 %s), "
 "расхождение с 37-м объявлено полем lagBehindGit; после коммита круга 49 будет залит 38-й слепок, а 37-й "
 "переименован и переведён в HOLD_superseded — имя снимка обязано быть правдой и по числу строк-носителей, и по "
 "байтам, и по md5 (правило 25)" % (b, l, md5))
dm["measuredAt"] = NOW
dm["checkedAt"] = NOW
COR.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус обновлён: байт", len(COR.read_bytes()))

IDX = pathlib.Path("/home/user/Research/ИСКУПЛЕНИЕ/data/atonement-library-index.json")
I = json.loads(IDX.read_text(encoding="utf-8"))
n2 = 0
for r in I["records"]:
    if r.get("role") == "registry-mirror" and r.get("driveId") == "1rCtYH83FjiVEhl4rzgdOmP500XzUFR8U":
        r["lagBehindGit"] = ("слепок #37 = дерево круга 48 (469418 B, md5 f4a7f749a1717271d0a6c69d7f95def1, 1447 "
 "строк, 209 строк-носителей); в дереве после круга 49 — %d B, md5 %s, %d строк при тех же 209 строках-носителях; "
 "имена и числа снимка не правятся (это история съёма), расхождение объявлено здесь, а переливка 38-го слепка — долг "
 "этого же круга" % (b, md5, l))
        lm = r["lagMeasured20261025r49"]
        lm.update({"treeBytes": b, "treeMd5": md5, "treeLines": l, "measuredAt": NOW, "checkedAt": NOW})
        r["checkedAt"] = NOW
        n2 += 1
assert n2 == 1
IDX.write_text(json.dumps(I, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("индекс обновлён: байт", len(IDX.read_bytes()))

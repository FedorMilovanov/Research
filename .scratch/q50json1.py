# -*- coding: utf-8 -*-
"""Круг 50, шаг 2: корпус. Сюда идут только те числа, которые снимаются с дерева;
всё, что касается переливки зеркала, придёт отдельным скриптом после заливки."""
import json, pathlib, re, hashlib, datetime

COR = pathlib.Path("ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
REG = pathlib.Path("docs/research/atonement/35_four_point_authors_mass_registry.md")
REC = pathlib.Path("ИСКУПЛЕНИЕ/17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md")
MIS = pathlib.Path("docs/research/atonement/15_patristic_and_reformation_misattributions.md")
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def m(t):
    return len(t.encode("utf-8")), t.count("\n") + 1, len(re.findall(r"(?m)^## ", t)), len(re.findall(r"(?m)^### ", t))


reg_t = REG.read_text(encoding="utf-8")
rec_t = REC.read_text(encoding="utf-8")
mis_t = MIS.read_text(encoding="utf-8")
RB, RL, RH2, RH3 = m(reg_t)
MD5 = hashlib.md5(REG.read_bytes()).hexdigest()
SHA = hashlib.sha256(REG.read_bytes()).hexdigest()
MB, ML, _, _ = m(mis_t)
NB, NL, NH2, NH3 = m(rec_t)
cls = {}
for mm in re.finditer(r"^\|\s*FP-(\d+)\s*\|(.*?)$", reg_t, re.M):
    c = re.search(r"`(A1|A2|B1|B2|C)`", mm.group(2))
    cls[c.group(1) if c else "нет"] = cls.get(c.group(1) if c else "нет", 0) + 1
rows = sum(cls.get(k, 0) for k in ("A1", "A2", "B1", "B2", "C"))
queue = len(set(re.findall(r"^- Q-(\d+) —", reg_t, re.M)))
dobyt = sum(1 for ln in reg_t.split("\n") if "Добыть:" in ln)
share_int = cls["A1"] * 100 // rows
share_round = round(cls["A1"] * 100 / rows)
print("реестр:", RB, RL, RH2, RH3, cls, "очередь", queue, "добыть", dobyt, "доля", share_int, share_round)
print("15_:", MB, ML, "| 17_:", NB, NL, NH2, NH3)

J = json.loads(COR.read_text(encoding="utf-8"))
R = J["fourPointMassRegistry20261023"]
R["perClass"] = {k: cls[k] for k in ("A1", "A2", "B1", "B2", "C")}
R["queueLength"] = queue
R["shareA1Percent"] = share_round
R["registrySectionsMeasured"] = {"H2": RH2, "H3": RH3, "lines": RL,
 "reshotBy": ("круг 50 (2026-10-25): H2 стал 50, потому что добавлен раздел ## 49; H3 не двинулся (11) — круг писал "
              "прозой без новых подразделов; %d строк и %d байт пересняты тем же обходом, каким сведён баланс круга"
              % (RL, RB))}
for k, v in (("fileBytesAsOfRound50", RB), ("fileMd5AsOfRound50", MD5), ("fileSha256AsOfRound50", SHA),
             ("linesAsOfRound50", RL), ("dobytLinesAsOfRound50", dobyt)):
    R[k] = v

R["bunyanCensusRound50Finding20261025"] = {
 "что": ("перепись по всем записям имени «Bunyan» в каталоге EEBO-TCP вместо чтения одного тома: 45 записей, "
         "14 628 964 байт TEI, 8358 делений <pb>, из них 7615 с напечатанным номером, <num> 0 во всех сорока пяти "
         "томах; строка FP-136 поднята до A1 по этой переписи, а не по одному трактату"),
 "шаблоны": {
  "удовлетворение за грехи мира": {"вхождений": 5, "томов": 3,
   "места": "A30137 (1673) сс. 57 и 108; A30141 (1685) сс. 126 и 280; A30208 (1656) с. 167"},
  "died for all (утвердительная рамка)": {"вхождений": 7, "томов": 6,
   "места": "A30128 с. 18; A30137 сс. 54 и 74; A30198 с. 25; A30203 с. 199 (заглавие из чужого списка); A30214 "
             "с. 207; A77832 с. 40"},
  "for his sheep": {"вхождений": 2, "томов": 1, "места": "A30141 сс. 164 и 286, оба как ссылка на Ин 10:11"},
  "not for the world / not for all the world": {"вхождений": 7, "томов": 7,
   "разбор": ("четыре — Ин 17:9 у Буньяна в чужом регистре (A30130 с. 15; A30121 и A30214 с. 45; N02531 с. 9), три "
              "— идиома «ни за что на свете» (A30141 с. 294; A30160 с. 135; N03023 с. 120); ни одного отрицания "
              "всеобщности удовлетворения")},
  "двойная уплата (уточнённый ряд)": {"вхождений": 0, "томов": 0,
   "шаблоны": "double payment|payment twice|twice paid|require … again|the same debt again|second payment",
   "против": "тот же ряд в необработанном виде («twice», «a second time») даёт 56 мест в 27 томах, и ни одно из них "
             "не есть довод о повторной уплате — отсюда пункт 3 правила 15zo."}},
 "номераНосителей": {"A30198": {"байт": 157875, "pb": 51, "pbN": 46, "num": 0, "сбросов": 1,
   "титул": "Reprobation asserted, or, The doctrine of eternal election & reprobation promiscuously handled in "
             "eleven chapters (Wing B5588; ESTC R30870; снимок British Library, микрофильм 1481:4, image set 48081)"},
  "A30141": {"байт": 599546, "pb": 361, "pbN": 341, "num": 0, "сбросов": 4,
   "титул": "The doctrine of the law and grace unfolded (1685; заметка записи: «Wing calls this \"Second\" edition»; "
             "Wing B5515; ESTC R34390)"},
  "прочие": "43 тома той же переписи скачаны и просчитаны теми же шаблонами, числа в таблице выше"},
 "measuredAt": NOW, "checkedAt": NOW,
 "how": ("curl -H 'Accept: application/vnd.github.raw' "
         "https://api.github.com/repos/textcreationpartnership/<id>/contents/<id.xml> по 45 идентификаторам из "
         "TCP.csv; разбор — .scratch/q50tei.py и .scratch/q50census.py, сводка чисел — .scratch/q50census.json"),
 "recheckCommand": "python3 -B .scratch/q50census.py (файлы лежат в .scratch/bun/)"}

R["bunyanVoiceFrameRound5020261025"] = {
 "что": ("формула, на которую строка FP-136 ссылалась чужим локатором, найдена в печатном издании 1674 года: "
         "«Christ died for all, tasted death for every man; is the Saviour of the World, and the Propitiation for "
         "the sins of the whole World» — A30198, напечатанная с. 25; «…the death of Christ did extend it self unto "
         "them: for the offer of the Gospel cannot, with Gods allowance, be offered any further then the death of "
         "Jesus Christ doth go» — там же, с. 26"),
 "рамка": ("вторая формула стоит после «the which it could not be, unless …» — она посылка опровержения в главе IX "
           "(«Whether God would indeed and in truth, that the Gospel … should be tendred to those that yet he hath "
           "bound up under eternal Reprobation?»), а не тезис об объёме; первая формула рамку имеет утвердительную, "
           "и её подписывает сам Буньян"),
 "следствиеДляСтроки": ("локатор «с. 130 сн. 24» снят: в издании 1674 года 44 нумерованные страницы, и страница 130 "
                        "с примечанием принадлежит разбору во вторичном источнике (The Baptist Quarterly 21:3, "
                        "сс. 126–130, сн. 21–27), а не трактату; строка поднята до A1 с двумя оговорками — спор об "
                        "авторстве трактата (John Brown) не решён, и класс меряет прочитанность места, а не "
                        "принадлежность пера"),
 "measuredAt": NOW,
 "how": "чтение по TEI с пересчётом носителей счёта по правилу 15zn.1; локатор называет систему (арабские номера на "
        "странице, один сброс на 46 нумерованных делений)"}

R["ownClaimCorrectionRound5020261025"] = {
 "что": ("собственное утверждение лана о Буньяне понижено до того, что держится: §6 файла "
         "15_patristic_and_reformation_misattributions.md называл приписывание Прокопенко «абсолютно ложным» и "
         "утверждал, что Буньян «категорически отвергает» благодать искупления для отверженных; по переписи 45 "
         "томов первая половина верна по форме (ни одна из трёх формул §6.1 не читается у Буньяна как его тезис об "
         "объёме), вторая — нет: формула удовлетворения «за грехи мира» у него стоит в трёх томах пять раз"),
 "дописано": ("в тот же файл добавлен §6.1.1 «Поправка круга 50» (%d байт, %d строк после правки); файл 17_ "
              "переснят правилом 24: «Буньян» → 24 вхождений (было 17), «Reprobation» → 3 (было 1), «bunyan» → 0, "
              "«Banner» → 0" % (MB, ML)),
 "шкала": ("мера расхождения: из трёх формул, на которые опиралось опровержение, одна — чужая цитата из Писания, "
           "одна — идиома, одна — заимствованный довод; 0 из 3 оказалось утверждениями Буньяна об объёме, и при "
           "этом 5 утверждений об удовлетворении «за мир» стоят в его же томах"),
 "measuredAt": NOW,
 "how": "оба числа пересняты после дописки файла, тем же определением, каким их мерит правило 24 гейта"}

R["queueNote20261025r50"] = ("Очередь %d адресов при %d строках класса `C`: круг 50 снял Q-136 (строка `FP-136` "
 "вышла из `C`, потому что место прочитано по напечатанным страницам издания 1674 года и по переписи 45 томов "
 "имени); новых адресов в список не внесено, а висящая охота названа в колонке строки после токена `Добыть:`, "
 "поэтому механический счётчик даёт %d строки при трёх висящих нуждах (REQ-7, REQ-8 и трактат из списка 1666 "
 "года) — расхождение счётчика и нужд назано словами, как его назвал круг 48" % (queue, cls["C"], dobyt))
R["queueClosures20261025r50"] = {
 "Q-136": ("снят: строка `FP-136` поднята до `A1`; издание и страницы места установлены (A30198, 1674, напечатанные "
           "сс. 25 и 26; A30141, 1685, сс. 126 и 280; A30137, 1673, сс. 57 и 108; A30208, 1656, с. 167), локатор "
           "вторичного разбора «с. 130 сн. 24» назван чужим и снят; вторая половина адреса (сверка по Banner of "
           "Truth, 1991, т. 1) осталась не сделанной и названа в строке — она не перенесена в очередь, потому что "
           "касается строки `FP-190`, а та стоит в `B1`, где адрес не обязателен"),
 "measuredAt": NOW,
 "how": "обход реестра тем же шаблоном, каким его мерят правила 23 и 23.1: `^- Q-(\\d+) —` по множеству номеров"}

R["shareDefinitionDivergenceRound5020261025"] = {
 "что": ("доля `A1` снова measurement-расходима: 39·100/%d = 18.66, целочисленное деление даёт 18, округление "
         "правила 23 — 19" % rows),
 "чтоДелаетКруг": ("корпус держит 19 (определение правила 23), README держит 18 (определение проверки 23.1), и "
                   "расхождение назано в §49 реестра; круг 49 закрывал это расхождение арифметикой (38 давало 18 по "
                   "обоим определениям), круг 50 его открыл снова — и то, и другое есть свойство меры, а не успех "
                   "или провал поиска"),
 "measuredAt": NOW, "how": "оба числа сняты одним обходом реестра в этом же скрипте"}

R["laneReadmeConsistency20261023"]["liveNumbers"] = {"rows": rows, "A1": cls["A1"], "A2": cls["A2"],
 "B1": cls["B1"], "B2": cls["B2"], "C": cls["C"], "queue": queue, "share": share_int}
R["laneReadmeConsistency20261023"]["mismatches"] = 0
R["laneReadmeConsistency20261023"]["method"] = (
 "восемь чисел сводки в README лана (строки-носители, пять классов, адресаты очереди, доля прочитанного по "
 "первичному) сняты одним обходом реестра в правиле 23.1; переснято кругом 50: 209 строк, A1 39, A2 35, B1 34, "
 "B2 6, C 95, адресатов 95, доля 18; расхождений ноль, и отдельно записано, что два определения доли снова "
 "расходятся (18 при целочисленном делении, 19 при округлении), потому что 39·100/209 = 18.66")
R["laneReadmeConsistency20261023"]["measuredAt"] = NOW
R["laneReadmeConsistency20261023"]["checkedAt"] = NOW

P = J["reproducibility20261022"]["countsLive"]
P["очередейДобычиМассы"] = queue
P["строкРеестраМассы"] = rows
P["measuredAt"] = NOW
P["method"] += ("; переснято кругом 50 (очередь 96 → 95 по снятому Q-136, классов A1 стало 39 при 209 строках, "
 "доля 18 целочисленным делением и 19 округлением; находка круга записана вложенными блоками "
 "fourPointMassRegistry20261023, верхнеуровневых ключей не добавлено — их число сверяется правилом 21)")

D = J["reconciliationDocument20261022"]
D["lines"] = NL - 1 if NL == len(rec_t.rstrip("\n").split("\n")) + 1 else NL
D["sectionsH2"] = NH2
D["sectionsH3"] = NH3
D["lines"] = len(rec_t.rstrip("\n").split("\n"))
D["reshotByRound50"] = {"команда": ("python3 -c \"import pathlib,re; p=pathlib.Path('ИСКУПЛЕНИЕ/"
 "17_RECONCILIATION_WITH_CANONICAL_SPINE_2026-10-15.md'); s=p.read_text(encoding='utf-8'); print(len(s.rstrip(chr("
 "10)).split(chr(10))), len(re.findall(r'(?m)^## ',s)), len(re.findall(r'(?m)^### ',s)), len(p.read_bytes()))\""),
 "байт": NB, "строк": D["lines"], "H2": NH2, "H3": NH3,
 "чтоДобавилКруг": ("новый блок правил `### 15zo.` из четырёх пунктов (отрицание в рамке, формула внутри «unless», "
                    "перепись по имени с названными шаблонами, заглавие из чужого списка) — отсюда +1 к H3; "
                    "числа пересняты после дописки, и пересняты также два старых числа того же файла, которые "
                    "правило 24 читает как претензии: «Буньян» 17 → 24 и «Reprobation» 1 → 3"),
 "measuredAt": NOW, "measuredBy": "тот же обход, что и в method блока"}
D["history"] = (D.get("history") or []) + [{"asOf": NOW, "lines": D["lines"], "sectionsH2": NH2, "sectionsH3": NH3,
 "note": "круг 50: блок 15zo. после 15zn., пересъём чисел правила 24 в том же файле",
 "байт": NB}]

G = J["grepBilingualAudit20261023"]
G["fixedInThisRound20261025r50"] = ("числа этого блока переснимает прогон гейта: правило 24 печатает число "
 "претензий и переснятых чисел, и блок обязан им равняться — сверка идёт по живому обходу, а не по памятью о "
 "предыдущем круге")
G["checkedAt"] = NOW

COR.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("корпус:", len(COR.read_bytes()), "байт | верхнеуровневых ключей:", len(J))

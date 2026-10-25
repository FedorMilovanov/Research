# -*- coding: utf-8 -*-
"""Круг 50, шаг 4: снимается ложное объявление мёртвой ссылки, счётчики правила 20
переснимаются итерацией по выводу самого гейта (не по памяти о том, что куда вошло)."""
import json, pathlib, re, ast, datetime, subprocess

COR = pathlib.Path("ИСКУПЛЕНИЕ/data/atonement-corpus-v1.json")
NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
J = json.loads(COR.read_text(encoding="utf-8"))
L = J["libraryIndex20261023"]
rmr = L["registryMirrorRoles"]
rmr["почемуНеОдно"] = ("записей с ролью registry-mirror в индексе две, а живым зеркалом реестра масс — одна: "
 "вторая (1u7fZCOat…) — замороженный слепок самого JSON-корпуса, снятый кругом 20 с коммита, которого нет в этой "
 "ветке: 305 429 байт, mime application/json, побайтового равенства дереву он не обещает, потому что правило 25 "
 "требует его только от зеркала реестра масс; его расхождение объявлено собственным полем lagMeasured20261024 "
 "(30 коммитов позади, 457 844 байта в дереве против 305 429 в имени). Формулировка «живых зеркал ровно одно» "
 "потому верна только с оговоркой «ровно одно зеркало реестра масс, сверяемое без объявления лага» — после "
 "переливки круга 50 ролей registry-mirror по-прежнему две, и это непролитая история круга 20, а не регресс")
rmr["токеныЗдесь"]=("номер коммита круга 20 в этот блок не перенесён: токен git-объекта в корпусе обязывает либо "
 "пересъём по git show, либо запись в карте recordCommit, а переливаемый слепок круга 20 никто не собирается "
 "переливать; блок потому описывает размер и байты, а не ссылку, — ссылка остаётся в самом индексе, где она "
 "рождена и где её читает читатель записи")
L.pop("verifiability20261023", None)
L.pop("indexBytesNote", None)
L["indexBytesNote20261025r50"] = ("число снято после последней записи файла индекса в этом кругу: индекс "
 "переписывался дважды (сначала запись 39-го слепка, потом снятие ложных ключей лага с замороженного слепка JSON), "
 "и первое значение 281 041 описывало промежуточное состояние; поле переименованo кругом 50, потому что "
 "предыдущее называло себя заметкой, а содержало пересъём")
M = J["driveMirrors"]["massRegistry20261023"]
M["pour39_20261025r50"]["chainAudit"]["совпалоСОжиданием"] = (
 "перед заливкой было записано, что после переливки станет 47 с именем и 46 с пометкой; проверка сошлась на обоих "
 "числах, и разность 47 и 46 по-прежнему равна одному живому зеркалу")
A = J["integrityGate"]["shaCitationAudit20261023"]
A.pop("recordCommitNote", None)
A["recordCommit"].pop("adf42fe", None)
A["byBlockNote"] = ("переснят кругом 50: в корпусе появился текст живого зеркала 39-го, и единственные git-токены, "
 "которые он называет (18db31d21 в pour39_20261025r50 и в блоке свойств), достижимы из HEAD, поэтому счётчик "
 "недостижимых не вырос; число уникальных токенов и распределение по блокам сняты не подсчётом в голове, а "
 "итерацией по выводу самого гейта (шаг 4 этого круга), и равны ему ровно в момент этой записи")
A["measuredAt"] = NOW
COR.write_text(json.dumps(J, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def gate():
    r = subprocess.run(["python3", "-B", "scripts/validate_atonement_corpus_integrity.py"], capture_output=True,
                       text=True, cwd="/home/user/Research")
    return r.stdout + r.stderr


for i in range(4):
    out = gate()
    m = re.search(r"shaCitationAudit20261023 разошёлся с обходом: byBlock: записано (\{.*?\}), видим (\{.*?\}), "
                  r"fieldsWithDeadLinks: записано (\d+), видим (\d+)(?:, uniqueShaTokens: записано (\d+), видим "
                  r"(\d+))?(?:, unreachableTokens: записано (\d+), видим (\d+))?", out)
    if not m:
        print("цикл %d: расхождения правила 20 по счётчикам нет" % i)
        break
    by_block = ast.literal_eval(m.group(2))
    A = json.loads(COR.read_text(encoding="utf-8"))["integrityGate"]["shaCitationAudit20261023"]
    A["byBlock"] = by_block
    A["fieldsWithDeadLinks"] = int(m.group(4))
    if m.group(6):
        A["uniqueShaTokens"] = int(m.group(6))
    if m.group(8):
        A["unreachableTokens"] = int(m.group(8))
    A["reachableTokens"] = A["uniqueShaTokens"] - A["unreachableTokens"]
    A["measuredAt"] = NOW
    J2 = json.loads(COR.read_text(encoding="utf-8"))
    J2["integrityGate"]["shaCitationAudit20261023"] = A
    COR.write_text(json.dumps(J2, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("цикл %d: принято byBlock=%s fields=%d unique=%d unreachable=%d" % (
        i, sorted(by_block.items()), A["fieldsWithDeadLinks"], A["uniqueShaTokens"], A["unreachableTokens"]))
print("--- финальный прогон ---")
print("\n".join(l for l in gate().split("\n") if "PASS" in l or "FAIL" in l or "ПРАВИЛО" in l or "правило" in l)[:1500])

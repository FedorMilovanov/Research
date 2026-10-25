# -*- coding: utf-8 -*-
"""Круг 50, шаг 1b: снимает адрес Q-136 из очереди и переснимает числа, вписанные в текст,
итерацией до неподвижной точки (число в абзаце меняет размер файла, размер меняет число)."""
import re, pathlib

REG = pathlib.Path("docs/research/atonement/35_four_point_authors_mass_registry.md")
MIS = pathlib.Path("docs/research/atonement/15_patristic_and_reformation_misattributions.md")


def occ(path, pat):
    return len(re.findall(re.escape(pat), path.read_text(encoding="utf-8"), re.I))


def measure(text):
    cls = {}
    for m in re.finditer(r"^\|\s*FP-(\d+)\s*\|(.*?)$", text, re.M):
        mm = re.search(r"`(A1|A2|B1|B2|C)`", m.group(2))
        k = mm.group(1) if mm else "нет"
        cls[k] = cls.get(k, 0) + 1
    rows = sum(cls.get(k, 0) for k in ("A1", "A2", "B1", "B2", "C"))
    q = len(set(re.findall(r"^- Q-(\d+) —", text, re.M)))
    dobyt = sum(1 for ln in text.split("\n") if "Добыть:" in ln)
    a1, a2 = cls.get("A1", 0), cls.get("A2", 0)
    return dict(rows=rows, A1=a1, A2=a2, B1=cls.get("B1", 0), B2=cls.get("B2", 0), C=cls.get("C", 0),
                queue=q, dobyt=dobyt, share=a1 * 100 // max(rows, 1), exact=a1 * 100 / max(rows, 1),
                pair=a1 + a2, pairpct=(a1 + a2) * 100 / max(rows, 1))


def nums(text):
    m = measure(text)
    m["cyr"] = occ(MIS, "Буньян")
    m["lat"] = occ(MIS, "bunyan")
    m["misbytes"] = len(MIS.read_bytes())
    m["mislines"] = MIS.read_text(encoding="utf-8").count("\n") + 1
    m["closePct"] = 7 * 100 / 102
    return m


def sub(pattern, repl, text, flags=0, must=True):
    new, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if must and n != 1:
        raise SystemExit("не найдено единственное вхождение шаблона: %s" % pattern[:70])
    return new


def main():
    t = REG.read_text(encoding="utf-8")
    # --- снимаем адрес Q-136
    t = sub(r"- Q-136 — Джон Буньян.*?\n", "", t, flags=re.S)
    for it in range(40):
        m = nums(t)
        old = t
        # байты и строки своего же файла — по тексту предыдущей итерации, цикл сходится к началу
        m["bytes"] = len(t.encode("utf-8"))
        m["lines"] = t.count("\n") + 1
        # (а) числа в строке FP-136
        t = sub(r"«Буньян» → \d+ вхождений по `15_patristic", "«Буньян» → %d вхождений по `15_patristic" % m["cyr"], t)
        t = sub(r"«bunyan» → \d+ вхождений по тому же файлу",
                "«bunьян» → %d вхождений по тому же файлу" % m["lat"], t).replace("«bunьян»", "«bunyan»")
        # (б) сводка очереди
        t = sub(r"очередь стала \d+, и это первое движение очереди",
                "очередь стала %d, и это первое движение очереди" % m["queue"], t)
        # (в) «Числа, названные с масштабом» и «Баланс круга» — пересобираем абзацы целиком
        d = dict(m, roundshare=round(m["exact"]), notpair=100 - m["pairpct"])
        para = ("**Числа, названные с масштабом.** Рядов-носителей позиции %(rows)d (строка не добавлена и не "
                "убавлена: круг менял класс, а не состав); `A1` — %(A1)d (было 38), то есть %(share)d %% от "
                "%(rows)d при определении, которым меряет README, и при обоих определениях, которые в этом круге "
                "**снова разошлись**: доля %(exact).2f, целочисленное деление даёт %(share)d, округление правила 23 "
                "— %(roundshare)d; расхождение названо, как его назвал круг 48, и README лана держит число "
                "целочисленного деления, потому что по нему сверяет проверка. `A2` %(A2)d, `B1` %(B1)d, `B2` "
                "%(B2)d, `C` %(C)d (было 96); очередь %(queue)d адресов (было 96: снят Q-136, не внесено ни "
                "одного); доля `A1`+`A2` = %(pair)d из %(rows)d, то есть %(pairpct).2f %%, остаток по шкале "
                "первичного свидетеля %(notpair).2f %%; доля очереди, закрытой тем, что уже лежит в лане, — 7 из "
                "102, то есть %(closePct).2f %% (было 5.88 %%: круг закрыл адрес, носитель которого лежал в "
                "`TCP.csv`, и это третий случай, когда очередь двигает не добыча, а перечитывание своего же "
                "индекса). Четыре тома открыты кругом целиком (A30198, A30141, A30137, A30208), полезными для "
                "строки оказались все четыре — 4 из 4, то есть 100.00 %% по шкале круга 49 («нашёл том — получил "
                "цитату»); шкала круга 49 потому и переснята здесь, что в этот раз поиск шёл не по фрагменту "
                "заглавия, а по всем записям имени: 45 томов, три дали утвердительную формулу удовлетворения, "
                "шесть — ряд «died for all», один том дал ложное отрицание, ни один не дал чужого довода о "
                "повторной уплате.\n\n") % d
        t = sub(r"\*\*Числа, названные с масштабом\.\*\* .*?\n\n", para, t, flags=re.S)
        bal = ("**Баланс круга:** файл реестра после правки занимает %(bytes)d байт и %(lines)d строк (было "
               "489 953 байта и 1 535 строк); строки-носители позиции %(rows)d; классы `A1` %(A1)d (+1), `A2` "
               "%(A2)d, `B1` %(B1)d, `B2` %(B2)d, `C` %(C)d (−1) — четвёртый сдвиг классов подряд и первый, где "
               "строка поднята не находкой в новом томе, а отказом от двух старых мер сразу; очередь %(queue)d "
               "адресов; `Добыть:` — %(dobyt)d строки по механическому счётчику (было 4: токен добавлен в строку "
               "`FP-136` как название библиографической охоты, и счётчик снова считает строки, а не нужды — "
               "висящих нужд 3: REQ-7, REQ-8 и эта охота, в список `REQ-` она не внесена, потому что список "
               "корпуса держит заявки на носители, а не заглавия из чужих списков). "
               "`15_patristic_and_reformation_misattributions.md` после поправки занимает %(misbytes)d байт и "
               "%(mislines)d строк. Числа сняты после дописки этого предложения и сходятся итерацией.\n") % d
        t = sub(r"\*\*Баланс круга:\*\* .*?сходятся итерацией\.\n", bal, t, flags=re.S)
        # заголовок H2: число разделов не вписано, но §49 обязан остаться одним
        if t == old:
            break
    REG.write_text(t, encoding="utf-8")
    left = re.findall(r"@[A-Z]+@", t)
    print("плейсхолдеры:", left)
    m = nums(t)
    print("итог:", {k: m[k] for k in ("bytes", "lines", "rows", "A1", "A2", "B1", "B2", "C", "queue", "dobyt",
                                      "share", "exact", "cyr", "lat", "misbytes", "mislines")})
    print("проверка байт/строк на записанном файле:", len(REG.read_bytes()),
          REG.read_text(encoding="utf-8").count("\n") + 1)


if __name__ == "__main__":
    main()

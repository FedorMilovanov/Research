# -*- coding: utf-8 -*-
"""Круг 48: правка реестра массы — три строки подняты по напечатанной странице,
три адреса сняты из очереди, четыре переписаны протоколом «читал, не нашёл»,
таблица ## 43 переснята, дописан раздел 47 с балансом-неподвижной точкой."""
import pathlib, re, sys

P = pathlib.Path("/home/user/Research/docs/research/atonement/35_four_point_authors_mass_registry.md")
T0 = P.read_text(encoding="utf-8")

ROW22 = ("| FP-22 | Брэдвардин, *De causa Dei, contra Pelagium* (том Сэвила держит «libri tres»: *De causa Dei* + "
 "*De virtute causarum*) | противоположный полюс: необходимость, предопределение, «за своих» | `A1` | имя «Henry "
 "George» в строке было слиянием двух имён титульного листа: том издал **Генри Сэвил** (*opera et studio Dr. Henrici "
 "Savilii*) по указанию архиепископа **Джорджа Эбботта** (*iussu reverendiss. Georgii Abbot Cantuariensis "
 "Archiepiscopi*), напечатан в **Лондоне** (Ex officina Nortoniana, apud Ioannem Billium), 1618, «ex scriptis "
 "codicibus nunc primum editi», сверка [34], 876 p.; EEBO-TCP A16626 = «STC 3534; ESTC S113557», 916 листов "
 "оцифровки, статус Free, транскрипция читается из этой среды (6 256 685 Б, напечатанная пагинация 1–876). **Круг 48 "
 "читает страницу: с. 250** — «Alij autem scientes, vel opinantes prædicta, non possunt, ut videatur, orare absolutè "
 "pro omnibus ut salventur; hoc enim ratio clare probat», и несколькими строками ниже: «si quandoque generaliter "
 "orant pro omnibus ut salventur, oportet quod tacitè saltem intelligant de omnibus prædestinatis ad vitam» — кто "
 "знает или полагает обратное, тот не может молиться о всех безусловно, потому что молитва без надежды быть "
 "услышанным противна разуму действующих; «все» здесь не отменяется, а читается молча как «все предопределённые к "
 "жизни». Соседняя **с. 242** — не его голос: там он приводит Августина (в его сноске «21 i. 24 o.», то есть *De "
 "correptione et gratia* quaest. 24? по счётке тома): «Ecclesia orat pro omnibus hominibus, nec tamen pro omnibus "
 "exauditur, sed pro his solis, qui etsi adversantur Ecclesiæ, ita sunt tamen prædestinati, ut pro eis exaudiatur», и "
 "реестр помнит разницу: это цитата, работающая в его пользу, а не его собственная формула. Номер книги «III», который строка несла "
 "со времён индекса, **снят**: единственный явный заголовок книги в томе 1618 г. («liber primus») стоит на с. 441, "
 "так что с. 250 лежит не там, где её предполагала строка, а сверить нумерацию книг по этому переплёту отсюда "
 "нельзя; локатор потому дан по напечатанной пагинации. Basel 1571 и London 1715 в единственном доступном индексе не "
 "представлены; 21 вхождение «pro omnibus» на 16 страницах (98, 242, 249, 250, 264, 274, 357, 359, 362, 406, 573, "
 "636, 657, 699 и ещё две) остаётся справкой для того, кто решит читать дальше, — очереди адрес больше не требует |")

ROW74 = ("| FP-74 | Дж. Тиллотсон, *Of sincerity and constancy in the faith and profession of the true religion, in "
 "several sermons* (London: printed for Richard Chiswell, 1695, «The sixth Edition corrected»; по подлинникам издал "
 "Ralph Barker) и *The remaining discourses, on the attributes of God* (London: printed for Ri. Chiswell, at the "
 "Rose and Crown in St. Paul's Church-yard, 1700, «the seventh volume») | линия «sincerity of God… offer to all»: "
 "Бог не хочет смерти грешника и хочет спасения всех, а распространение его благорасположения условно | `A1` | "
 "EEBO-TCP A62570 = «Wing T1204; ESTC R17209» (492 листа оцифровки, транскрипция 618 205 Б) и A62579 = «Wing T1216; "
 "ESTC R222200» (440 листов, 574 737 Б), обе записи Free; нумерация `<pb n=>` в обоих томах = напечатанная. **Круг "
 "48 читает страницы: A62570, с. 366** (конец проповеди на Hebr. 10 — следующая проповедь на Matth. 16:24 "
 "открывается уже с. 367): «every Man ought to have better Thoughts of God, than to believe, that he, who "
 "delighteth not in the death of sinners, and would have all men to be saved and come to the knowledge of the truth, "
 "will confirm the Sentence of such uncharitable Men, as take upon them to condemn Men for those things, for which "
 "our Saviour in his Gospel condemns no Man» — формула 1 Тим 2:4 стоит в собственном голосе Тиллотсона и служит ему "
 "аргументом против самоуверенного осуждения; **A62579, с. 44** (проповедь II «The Goodness of God» на Ps. 145:9, "
 "по оглавлению тома страницы 25–50): «this Affection of God is common to all Men (tho' of all Creatures we have "
 "least deserved it) and is ready to diffuse and shed abroad it self, wherever Men are qualified for it by Duty and "
 "Obedience, and do not obstruct and stop the emanations of it, by their Sins and Provocations» — то есть «offer to "
 "all» держится у него на условии, а не на всеобщем декрете. Прежняя редакция строки требовала *Works* (London 1752) "
 "и искала на странице фразу «universal redemption»; круг 48 снимает и то и другое: во всех доступных томах "
 "проповедей эта фраза не встречается ни разу (0 вхождений, как и «offer to all»), а том 1752 г. строке больше не "
 "нужен — печати 1695 и 1700 гг. старше и держат нужные страницы |")

ROW78 = ("| FP-78 | Г. Уитфилд, *The Querists. The Rev. Mr. Whitefield's Answer, the Rev. Mr. Garden's Letters, &c.* "
 "(New York: printed by J. P. Zenger, 1740; на обороте «Printed in the Year M,DCC,XL.») | противоположная сторона, "
 "обязательная для объективности: Уитфилд публично отказывается от всеобщего искупления | `A1` | EEBO-TCP N03743 = "
 "«Evans 4588», «viii, 9-160 p.», 161 страница оцифровки, статус Free; в записи рядом с Уитфилдом — Alexander Garden "
 "и пресвитерианские общества; транскрипция читается из этой среды (261 865 Б), нумерация `<pb n=>` = напечатанная "
 "(9–160). **Круг 48 читает страницу: с. 64** — «In my Sermon on Justification, I seem to assert universal "
 "Redemption, which I now absolutely deny.» — в ряду самопоправок: «These, and perhaps some other Passages, tho' "
 "capable of a candid Interpretation, I now mislike, and in the next Edition of my Sermons, God willing, I propose to "
 "alter them»; там же названа строка «Marks of the new Birth»: «We shall endure to the End, if we continue» — то "
 "самое условное придаточное, из-за которого его и поправляли. Строка больше не ждёт ни *Works* (ed. S. J. Tyler, "
 "1871?), ни «Journal, 1739–44»: ответ на письма напечатан в 1740 г., он короче и доступен; вопрос «на какой именно "
 "„Letter to Mr. W.?\" отвечает Уитфилд» снят — это письма Alexander Garden'а, собранные в том же томе. Соседний "
 "N03645 = *The Rev. Mr. Whitefield's answer. To the Bishop of London's last pastoral letter* (Evans 4457, 1739, 24 "
 "листа) прочитан кругом 48 целиком: «universal redemption» в нём нет, а единичные «all men» и «answer» сидят на "
 "титульной странице |")

Q58 = ("- Q-58 — Престон. Круг 48 переписывает адрес по автору, а не по заглавию: в каталоге 33 записи «Preston, "
 "John, 1587-1628», почти все Free; прочитаны три тома — A09997 *Remaines* (1634, «STC 20249», 405 л.), A09990 "
 "*The nevv covenant, or the saints portion* (1629, «STC 20241», 626 л.) и A09950 *The breast-plate of faith and "
 "love* (1630, «STC 20208», 606 л.). Ни в одном нет ни «woulde/will have all men», ни условной формулы всеобщего "
 "желания спасения: «all men» у Престона стоит в увещании («it may serve for exhortation to all men, that they would "
 "labour to grow strong in the inward man», A09997, с. 95), а «condition» (48, 100 и 101 вхождение) — о честности "
 "Авраама и о «состоянии» кающегося, не о гипотетическом завете. Значит ярлык «английский гипотетический "
 "универсализм до Амираута» — характеристика Криспа, а не фраза Престона: адрес остаётся `C`, и искать в нём нужно "
 "не фамилию и не «Works (London 1634?)», а условное придаточное («if they believe», «if we continue») в названной "
 "проповеди, с томом и страницей.")

CL64 = (" Круг 48 переписывает и этот адрес по автору: «Nye, Philip, 1596?-1672» даёт в каталоге 33 записи; прочитан "
 "A12183 = *The excellencie of the Gospell above the law* (1639, «STC 22492», 668 л., Free), записанный под тремя "
 "именами — Sibbes, Goodwin, Nye: «all men» там 10 вхождений, все о христианской свободе и утешении, «condition» 40 "
 "— об обетовании; возражений Ассембли о всеобщности в томе нет, а самих *Minutes of the Westminster Assembly* "
 "каталог не держит ни под одним автором.")

CL164 = (" Круг 48 читает и второй английский том Занки, найденный по фамилии: A15859 *Speculum Christianum* (1614, "
 "перевод «By H.N.», в каталоге Henry Nelson, «STC 26121A.7; ESTC S111786», 404 л., статус Restricted, но TEI "
 "читается). О любви Божией там сказано: «it is nothing else but the free love of God, eternall and vnchangeable "
 "towards his Elect» (с. 121) и «as the love of God is spread abroad in our hearts, not by free will which ariseth "
 "out of vs, as saith Augustine, but by the spirit which is giuen vnto vs» (с. 112) — различие «love toward the "
 "Elect» приписывается строкой именно Занки, и он его действительно держит; но её формулы («he loves not all things "
 "with an equal love», «God loves all things which he has made besides himself») в этом томе отсутствуют (по нулю "
 "вхождений), как и в A97309. Адрес потому остаётся: нужны латинские folio *De natura Dei* / *Operum* — или "
 "указание, какой английский сборник держит главы о любви.")

CL11 = (" Круг 48 по фамилии находит в каталоге четыре печатных тома Ратрамния (A02359 *Three rare monuments of "
 "antiquitie*, 1624, Free, 152 л.; A10468, 1548, 36 л.; A10472, 1623, 122 л.; A27524, 1688, 521 л., латынь с новым "
 "английским переводом и историческим исследованием о авторе) — и все четыре держат *De corpore et sanguine*, не *De "
 "prædestinatione*: ложная надежда «средневековый трактат по-английски уже напечатан» снята, адрес остаётся.")

SEC = """
## 47. Круг 48 (25.10.2026, вечер после круга 47): перепись по автору вместо переписи по заглавию — три строки подняты по напечатанной странице, девять опознаний сняты

**Зачем этот круг.** Круг 47 нашёл канал (`textcreationpartnership/<TCP-id>`: полный TEI читается через `api.github.com`) и поднял в этом канале две строки; владелец сказал «Продолжай». У круга 47 осталось два неисполненных обещания: снять локатор Брэдвардина по 21 вхождению «pro omnibus» и переписать долю адресов, для которых первичный текст достижим, **по автору, а не по фрагменту заглавия**. Оба исполнены здесь, и второе оказалось важнее первого.

**Перепись по автору.** Таблица `TCP.csv` (61 315 записей) просеяна по подстрочнику фамилии в столбце `Author`. Число записей на фамилию: Whitefield 64, Tillotson 62, Preston 33, Nye 33, Chillingworth 16, Williams (Daniel, 1643?–1716) 14, Ratramnus 4, Zanchi 4, Bradwardine 1 — и нули там, где строки чего-то ждут: Wardlaw 0, Alexander 0, Prudentius 0, Haymo 0, Paschasius 0, Godescalcus 0. Осторожность нужна и с самим счётом: «Prosper» даёт 12 записей, и все ложны (подстрока из «vnhappy prosperitie», «a prosper fall»), — подстрочник фамилии так же опасен, как подстрочник заглавия. Практический вывод один: **число 66 «адресов без записи» — артефакт способа поиска**, а не состояние источниковой базы.

**Разбор десяти адресов, намеченных кругом 47 как цитируемые** (шкала: совпадает ли найденная запись с тем трудом, о котором строка). Правильную работу держит **один из десяти**, то есть 10.00 %:

| адрес | куда вела перепись по фрагменту заглавия | чем это оказалось | что дала перепись по фамилии |
|---|---|---|---|
| Q-02 (Проспер) | A00075 | *Capitula siue constitutiones ecclesiasticæ*, кентерберийский синод 1597 г. — зацепка за слово «Capitula» из строки | 12 записей с «prosper», все ложны; патристика вне охвата каталога |
| Q-12 (Пруденций Троаский) | A00402 | *Wonderfull newes of the death of Paule the iii.* (Matthias Flacius, 1552) | 0 записей |
| Q-22 (Брэдвардин) | A16626 | **верно**: том Сэвила, Лондон 1618 | 1 запись — он же; строка закрыта страницей |
| Q-58 (Престон) | A02836 | *Quodlibets lately come ouer from New Britaniola* (Robert Hayman, 1628) | 33 записи; A09997, A09990, A09950 прочитаны — формул строки нет |
| Q-64 (Нее) | A85742 | ответ «G. G.» о речи Чэлонера (1642), совпавший с фразой «interest of the kingdome», которую круг 46 сам вписал в адрес | 33 записи; A12183 прочитан — возражений Ассембли нет |
| Q-74 (Тиллотсон) | K008295.001 | *The Rambler* Сэмюэла Джонсона — совпадение по году 1752 | 62 записи; A62570 (1695) и A62579 (1700) прочитаны → строка закрыта |
| Q-78 (Уитфилд) | N03638 | *Christmas well kept, and the Twelve Days well spent* — автор верный, труд не тот | 64 записи; N03743 прочитан → строка закрыта |
| Q-81 (Уордлоу) | A58146 | *Blessedness, or, God and the world weighted in the balances of the sanctuary* (Francis Raworth, 1656) — зацепка за слово «Balances» | 0 записей; 1805–1817 вне охвата |
| Q-164 (Занки) | A97309 | верные автор и переводчик, не тот трактат | 4 записи; A15859 прочитан — формул строки нет |
| Q-167 (А. Александр) | A02641 | *The repentance of Iohn Haren priest* (1610) | 0 записей; 1868 вне охвата |

**Попаданий цитат — ноль.** Гибкий поиск (нормализация `ſ`, лигатур, `Æ`/`Œ`, ударных гласных и переносов в конце строки) по десяти кэшированным файлам даёт два попадания, и оба на титульной странице: «nunc primum editi» и «interest of the kingdome» — эхо слов, которые круг 46 сам вписал в адреса очереди. В теле напечатанного текста попаданий **0 из 10 (0.00 %)**. Отсюда правило, вынесенное в `### 15zm.`: попадание на титуле — не попадание, а каталожное заглавие, совпавшее со словами строки, — не идентификация труда.

**Что всё-таки читается.** Все три строки, которые круг поднимает, закрыты не поиском цитаты, а чтением страницы, найденной по смысловому якорю: Брэдвардин (с. 250: молиться «за всех» разумно лишь о предопределённых), Уитфилд (с. 64: «I seem to assert universal Redemption, which I now absolutely deny»), Тиллотсон (A62570, с. 366: «would have all men to be saved»; A62579, с. 44: благорасположение «common to all Men» при условии «Duty and Obedience»). Отсюда неприятный для метода вывод: **место надо искать по теме, а цитату находить уже там** — строки были правы по существу и ошибались в выходных данных, поэтому поиск по их собственным словам не привёл бы никуда.

**Что круг снимает с себя.** С FP-22 снят номер книги («III»), унаследованный от индекса: в томе 1618 г. на с. 250 он не читается; с FP-74 снято требование *Works* 1752 г. и приписанная строке фраза «universal redemption» (0 вхождений); с FP-78 снято ожидание *Works* под редакцией Тайлера 1871 г. и вопрос о том, на какое письмо отвечает Уитфилд. Ни один класс не понижен: отзыв опознания возвращает строку в прежнее «печатной основы нет», и в восьми адресах очереди это записано словами «круг 48: ложная запись».

**Что осталось в очереди.** Q-58, Q-64 и Q-164 переписаны так, чтобы следующий круг не повторял этот поход: в них названы прочитанные тома и отсутствующие формулы. Q-11 получил снятие ложной надежды (четыре напечатанных тома Ратрамния держат *De corpore et sanguine*, не *De prædestinatione*). «Добыть:» остаётся 2 — REQ-7 (принадлежность цитат переводу Уинертона) и REQ-8 (Cunningham, pp. 333–370, закрытый доступ HathiTrust).

**Числа, названные с масштабом.** Из 209 строк прочитаны по первичному свидетелю 37, то есть 17.70 % (было 34, 16.27 %); строк без первичного свидетеля 97, то есть 46.41 % (было 47.85 %); очередь сократилась с 100 до 97 адресов, и за два круга из 102 адресов закрыто 5 — 4.90 %, остаток 95.10 %. Это те же шкалы, что в §43 и §46; новых шкал круг не вводил.

"""

BAL = ("**Баланс круга:** файл реестра после правки занимает {B} байт и {L} строк (было 448 944 байта и 1 418 строк); "
 "строки-носители позиции 209; классы `A1` {a1} (+3), `A2` 35, `B1` 34, `B2` 6, `C` {c} (−3) — второй сдвиг классов "
 "подряд и первый, где подняты три строки разом; очередь {q} адресов (было 100: сняты Q-22, Q-74 и Q-78, не внесено "
 "ни одного — крупнейшее сокращение с круга 21); доля очереди, закрытая тем, что уже лежит в лане, — 5 из 102, то "
 "есть {pq} %, остаток {pqr} %; доля `A1` — {p1} % от 209 (было 16 %), доля `A1`+`A2` — {p2} % (было 33 %), остаток "
 "по шкале первичного свидетеля — {p3} % (было 83.73 %); из десяти адресов, намеченных кругом 47 как цитируемые, "
 "правильную работу держит {ok} — {pok} %, а реальных попаданий цитат в теле напечатанного текста — 0, то есть "
 "{pqu} %; `Добыть:` — 2. Числа сняты после дописки этого предложения и сходятся итерацией.")


def measure(t):
    a1 = a2 = b1 = b2 = c = rows = 0
    for ln in t.split("\n"):
        if not re.match(r"^\| FP-\d+ \|", ln):
            continue
        rows += 1
        m = re.match(r"^\| FP-\d+ \|[^|]*\|[^|]*\|[^|]*\|[^|]*\|", ln)
        k = re.findall(r"`(A1|A2|B1|B2|C)`", m.group(0) if m else "")
        if k:
            k = k[0]
            a1 += k == "A1"; a2 += k == "A2"; b1 += k == "B1"; b2 += k == "B2"; c += k == "C"
    q = len(re.findall(r"^\s*-\s*Q-\d+\s*—", t, re.M))
    return rows, a1, a2, b1, b2, c, q


def grp(txt, pat, new, name):
    n = len(re.findall(pat, txt, re.M))
    if n != 1:
        sys.exit("FAIL %s: шаблон встретился %d раз" % (name, n))
    return re.sub(pat, new if callable(new) else new.replace("\\", "\\\\"), txt, count=1, flags=re.M)


t = T0
for fp, new in (("FP-22", ROW22), ("FP-74", ROW74), ("FP-78", ROW78)):
    t = grp(t, r"^\| %s \|[^\n]*$" % fp, new, "row " + fp)
for qq in ("22", "74", "78"):
    pat = r"^\s*-\s*Q-%s\s*—[^\n]*\n" % qq
    if len(re.findall(pat, t, re.M)) != 1:
        sys.exit("FAIL снятие Q-%s" % qq)
    t = re.sub(pat, "", t, count=1, flags=re.M)
t = grp(t, r"^\s*-\s*Q-58\s*—[^\n]*$", Q58, "Q-58")
t = grp(t, r"^\s*-\s*Q-64\s*—[^\n]*$", lambda m: m.group(0) + CL64, "Q-64")
t = grp(t, r"^\s*-\s*Q-164\s*—[^\n]*$", lambda m: m.group(0) + CL164, "Q-164")
t = grp(t, r"^\s*-\s*Q-11\s*—[^\n]*$", lambda m: m.group(0) + CL11, "Q-11")
if t.count("Очередь стала 100. Ни разу") != 1:
    sys.exit("FAIL §17 якорь")
ins = ("Очередь стала 100.\nКруг 48 снял три адреса (Q-22, Q-74, Q-78: строки FP-22, FP-74 и FP-78 переведены в "
       "`A1`, потому что место прочитано по напечатанной странице тома — A16626, с. 250; A62570, с. 366 и A62579, "
       "с. 44; N03743, с. 64), новых адресов не внёс ни одного: очередь стала 97, и это крупнейшее сокращение с "
       "круга 21. Ни разу")
t = t.replace("Очередь стала 100. Ни разу", ins, 1)
t = grp(t, r"^\| строки реестра с первичным свидетелем \([^\n]*$",
        "| строки реестра с первичным свидетелем (`A1` из 209) | 209 | 32 → 34 → **37** (ряд переснят кругами 47 и "
        "48) | **84.69 % → 83.73 % → 82.30 %** |", "таблица, ряд 1")
t = grp(t, r"^\| строки, прочитанные по первичному[^\n]*\| 209 \|[^\n]*$",
        "| строки, прочитанные по первичному или сверенные по изданию (`A1`+`A2`) | 209 | 67 → 69 → **72** | "
        "67.94 % → 66.99 % → **65.55 %** |", "таблица, ряд 2")
t = grp(t, r"^\| строки без первичного свидетеля[^\n]*$",
        "| строки без первичного свидетеля (`C`) | 209 | — | 48.80 % → 47.85 % → **46.41 %** шкалы занято "
        "очередью |",
        "таблица, ряд 3")
t = grp(t, r"^\| адреса очереди, закрытые тем[^\n]*$",
        "| адреса очереди, закрытые тем, что уже лежит в лане | 102 | 2 → 0 → 2 → **5** (круг 47 снял Q-65 и Q-67, "
        "круг 48 — Q-22, Q-74 и Q-78; при строгом своде «имя + название + локатор + цитата» два адреса круга 43 "
        "остались полуготовностью по общему слову) | **98.04 % → 100 % → 98.04 % → 95.10 %** |", "таблица, ряд 4")
t = t.rstrip("\n") + "\n" + SEC.strip("\n") + "\n@@BAL@@\n"

base = re.sub(r"\n@@BAL@@\s*$", "", t.rstrip("\n"))
bal = BAL
for it in range(80):
    cand = base + "\n" + bal + "\n"
    rows, a1, a2, b1, b2, c, q = measure(cand)
    sp = lambda x: f"{x:,}".replace(",", " ")
    pc = lambda a, b: f"{100 * a / b:.2f}"
    nb = len(cand.encode())
    nl = len(cand.rstrip("\n").split("\n"))
    newb = BAL.format(B=sp(nb), L=sp(nl), a1=a1, c=c, q=q, pq=pc(5, 102), pqr=pc(97, 102),
                      p1=pc(a1, rows), p2=pc(a1 + a2, rows), p3=pc(rows - a1, rows),
                      ok=1, pok=pc(1, 10), pqu=pc(0, 10))
    if newb == bal:
        break
    bal = newb
else:
    sys.exit("FAIL: баланс не сошёлся за 80 итераций")
t = t.replace("@@BAL@@", bal)

rows, a1, a2, b1, b2, c, q = measure(t)
assert rows == 209 and (a1, a2, b1, b2, c) == (37, 35, 34, 6, 97) and q == 97, (rows, a1, a2, b1, b2, c, q)
assert c == q, "правило 23: C-строк должно быть столько же, сколько адресов"
for fp, yrs in (("FP-22", "1618"), ("FP-74", "1695"), ("FP-78", "1740")):
    ln = re.search(r"^\| %s \|[^\n]*$" % fp, t, re.M).group(0)
    assert "`A1`" in ln and yrs in ln and "с. " in ln, fp
assert "De causa Dei contra Pelagium* III" not in t
for qq in ("22", "74", "78"):
    assert not re.search(r"^\s*-\s*Q-%s\s*—" % qq, t, re.M), qq
assert "заливкиProperties" not in t
CJK = r"[\u3040-\u30ff\u4e00-\u9fff]"
assert len(re.findall(CJK, t)) == len(re.findall(CJK, T0)), "новая CJK попала в реестр"
assert not re.search(CJK, SEC + ROW22 + ROW74 + ROW78 + Q58 + CL64 + CL164 + CL11 + BAL), "CJK в моих строках"
for tok in ("workìng","grammar","eight местах","Счён","quoting"):
    assert tok not in t, tok
nb = len(t.encode()); nl = len(t.rstrip("\n").split("\n"))
assert ("**Баланс круга:** файл реестра после правки занимает %s байт и %s строк" %
        (f"{nb:,}".replace(",", " "), f"{nl:,}".replace(",", " "))) in t, "баланс не сходится с фактом"
P.write_text(t, encoding="utf-8")
print("OK: байт %d строк %d | ряды %d | классы A1 %d A2 %d B1 %d B2 %d C %d | очередь %d" %
      (nb, nl, rows, a1, a2, b1, b2, c, q))

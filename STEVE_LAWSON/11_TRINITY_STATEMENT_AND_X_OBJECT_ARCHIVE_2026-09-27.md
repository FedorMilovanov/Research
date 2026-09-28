# Steven J. Lawson — заявление Trinity (реконструкция текста), статус X-объекта, персистентность OnePassion, Banner of Truth


> **Status note (2026-09-28):** This file is a **historical pre-closure snapshot**. Its statement that the Trinity original was still open was superseded when `12_` located the archived official homepage object. Current operational status is `19_CURRENT_STATUS_AND_ACQUISITION_QUEUE_2026-09-28.md`.
**Corpus:** LAWSON-2024-2026
**Snapshot:** 2026-09-27 (поздний вечерний проход)
**Status:** дополнение к [`10_BOOK_SAMPLE_PAGES_ADDENDUM_2026-09-27.md`](10_BOOK_SAMPLE_PAGES_ADDENDUM_2026-09-27.md); новых первичных объектов о самом падении нет — уточнена доказательная база институциональных заявлений
**Companion:** [`02_SOURCE_LEDGER_2026-09-27.md`](02_SOURCE_LEDGER_2026-09-27.md) (§R), [`DURABLE_CUSTODY_MANIFEST.json`](DURABLE_CUSTODY_MANIFEST.json)

Этот проход закрывает два пробела, которые до сих пор держали важные цитаты в «серой зоне»:

1. **Текст заявления Trinity от 19.09.2024 реконструирован по пяти независимым носителям** — с пофразной атрибуцией. Ранее в корпусе была только суть; теперь есть дословные фразы, включая те, которых в корпусе не было вовсе.
2. **Установлен фактический статус архива X-заявления от 12.03.2025**: у Wayback есть минимум 8 снимков URL (первый — через два дня после публикации), но текст в них не сохранился; снимки июля–августа 2025 отдают служебную страницу X «страница не существует».

---

## 1. Объекты

| ID | Объект | Класс | Доступ | Примечание |
|---|---|---|---|---|
| SL-O01 | **Заявление старейшин Trinity Bible Church of Dallas от 19.09.2024** — реконструкция текста по пяти независимым носителям: Christian Post (20.09.2024), CHVN Radio (Manitoba), The Independent (20.09.2024), WFAA (Dallas), Distractify; плюс Banner of Truth (14.10.2024) как шестой носитель | A3 через B1-носители (оригинальная страница по-прежнему отсутствует) | FULL_TEXT_RECONSTRUCTED (пофразная атрибуция) | Снимки: `cp_statement.html` (63 998 B), `chvn.html` (66 962 B), `independent.html` (244 770 B); sha256 в манифесте |
| SL-O02 | **Banner of Truth**, Warren Peel, «When a Christian Leader Falls», 14.10.2024 — институциональный разбор (12 пунктов), цитирующий оба заявления | B1 (институциональная комментария) | FULL_OBJECT_VERIFIED (текст получен извлечением; прямой `curl` → HTTP 403, защита от ботов) | Локатор: `banneroftruth.org/us/resources/announcements/2024/when-a-christian-leader-falls/` |
| SL-O03 | **Wayback: снимки X-поста** `1899912459521319253` — 8 моментов в timemap; первый `20250314055735` (14.03.2025, через два дня после публикации) | A1-носитель (URL), текст не сохранён | URL_LEVEL_ARCHIVED / TEXT_LEVEL_MISSING | Снимки 2025-03-14 и 2025-03-21 — JS-оболочки X без текста; проверено `id_`-сырьё |
| SL-O04 | **Wayback: снимки 2025-07-06 и 2025-08-16 того же URL** — отдают страницу X «Nothing to see here… Looks like this page doesn't exist» | Состояние объекта | PAGE_STATE (наблюдение) | Осторожно: фиксируем как «на эти даты URL отдавал страницу несуществования», без вывода «удалено автором» |
| SL-O05 | **OnePassion: второй снимок заявления** — захват `20250123081434`; страница «OnePassion Public Statement» с текстом «…a sin that has disqualified him from ministry…» | A3 (page-state) | FULL_OBJECT_VERIFIED | Значит, заявление оставалось опубликованным минимум до 23.01.2025 (≈4 месяца после падения) |
| SL-O06 | Негативные результаты (архивы/инфраструктура) | — | NEGATIVE_RESULT | archive.today: 429/без ответа по всем зеркалам; timetravel (memento): соединение не устанавливается; xcancel (nitter-зеркало): HTTP 451; nitter.net / nitter.poast.org: недоступны; `tms.edu` в Wayback снимков не имеет; у домена церкви только снимок 2019 года |

Байтовые копии — `_work/custody_20260927c/` (вне Git; `SHA256SUMS.txt`, `SHA256SUMS_X.txt` внутри).

---

## 2. Реконструкция заявления Trinity (verbatim, пофразно)

> **Как читать.** Каждая фраза — дословная цитата из носителей ниже; в скобках — кто её приводит. Оригинальная страница церкви в архивах отсутствует, поэтому класс — «A3 через B1-носители»: цитировать допустимо **с атрибуцией заявлению старейшин Trinity (19.09.2024) и указанием, что текст приводится по публикациям носителей**.

1. «The elders at Trinity Bible Church of Dallas regretfully announce that effective immediately, Steven J. Lawson has been removed indefinitely from all ministry activities at Trinity Bible Church of Dallas.» — *Christian Post, WFAA, CHVN, Independent, Banner of Truth*
2. «Several days ago, the elders at Trinity Bible Church of Dallas were informed by Steve Lawson of an inappropriate relationship that he has had with a woman.» — *Christian Post, WFAA, CHVN, Banner of Truth*
3. «The elders have met with Steve and will continue to come alongside him and pray for him with the ultimate goal of his personal repentance.» — *все пять*
4. «Steve will no longer be compensated by Trinity Bible Church of Dallas.» — *все пять*
5. «In light of this, may we be reminded that we are ALL sinners, and Jesus Christ came into the world to save sinners — and Christ remains Head of His Church, which is bigger than any fallen man.» — *Christian Post, CHVN* **(в корпусе отсутствовало)**
6. «Jesus Christ will continue to lead His Church, including Trinity Bible Church here in Dallas, just like He has from the start of this work.» — *CHVN* **(в корпусе отсутствовало)**
7. «The Lord was building Trinity Bible Church of Dallas well before Steve became our Lead Preacher, and He will continue to build this church long after Steve Lawson, or any other man for that matter.» — *Christian Post, CHVN, Chron* **(в корпусе отсутствовало)**
8. «We would ask for your prayers for the elders, for our Body, and for Steve and his family. Let us always be mindful of the words of 1 Corinthians 10:12: “Therefore let him who thinks he stands take heed that he does not fall.”» — *The Independent* **(в корпусе отсутствовало)**

**Наблюдение о носителях.** Разные издания обрывают цитату в разных местах (Banner of Truth — на п. 4; The Independent — на пп. 3–4 и п. 8; Christian Post и CHVN — на пп. 5–7). Это типичная картина для заявления, распространявшегося текстом; совпадение формулировок там, где носители перекрываются, — взаимное подтверждение. Пункты 1–4 подтверждены ≥5 независимыми носителями; пункты 5–8 — 1–3 носителями каждый; для них в статье желательно держать формулировку «по публикации такого-то издания».

---

## 3. Что это меняет

- Раздел статьи о реакции церкви можно теперь строить не на пересказе, а на **дословных фразах самого заявления** — включая ту, что задаёт богословскую рамку всего эпизода: «Christ remains Head of His Church, which is bigger than any fallen man», и ту, что отделяет служение от личности: «…long after Steve Lawson, or any other man for that matter».
- Курсив корпуса «Троица — ведущий проповедник, не старейшина» остаётся в силе; заявление само называет его «Lead Preacher», что подтверждает редакционную норму.
- Ограничение P0 не снято: **оригинальный объект (страница/пост церкви) по-прежнему не найден**; реконструкция — это шесть носителей, а не сам объект.

---

## 4. Статус X-заявления (12.03.2025): что установлено точно

**Установлено (архивное состояние):**

- у Wayback есть **8 снимков URL** поста; первый — `20250314055735` (14.03.2025), то есть через два дня после публикации;
- снимки марта 2025 (14.03 и 21.03) — **JS-оболочки X**: текста заявления в них нет (проверено и в обычном, и в `id_`-сырьевом режиме);
- снимки **06.07.2025 и 16.08.2025** отдают служебную страницу X «Nothing to see here… Looks like this page doesn’t exist»;
- страница аккаунта в Wayback (снимки 20.09.2024, 21.03.2025, 24.03.2025) — тоже оболочки без текста.

**Чего устанавливать нельзя:** что пост удалён именно автором и именно тогда; что он недоступен сегодня (проверка живого X из песочницы невозможна — nitter-зеркала и archive.today недоступны, см. SL-O06). Формулировка для статьи: «текст заявления сохранился в публикациях носителей; архивные копии самого поста текста не сохранили, а более поздние архивные снимки URL отдают страницу несуществования».

**Что остаётся в силе:** дословный текст заявления (в т.ч. «sinned grievously… a sinful relationship with a woman not my wife… I alone am responsible… redemption and restoration in our marriage») доступен через носители B1 и уже учтён в корпусе (SL-A05/SL-D06).

---

## 5. Персистентность заявления OnePassion

Второй независимый снимок (23.01.2025) показывает, что заявление оставалось опубликованным на сайте OnePassion спустя четыре месяца после падения — в отличие от X-поста. Для статьи это существенная деталь: институциональный текст не был снят, то есть «исчезновение» относится к личному заявлению на платформе, а не к заявлению организации.

---

## 6. Banner of Truth: институциональный голос для баланса

Разбор Уоррена Пила (Banner of Truth, 14.10.2024) — редкий пример **институциональной** (не таблоидной и не партийной) реакции. Что из него полезно:

- он прямо цитирует оба заявления и призывает «mourn with those who mourn», включая «семью другой женщины, их церкви и друзей»;
- он формулирует границу, которую корпус сам держит: «a fallen Christian is still a Christian», и одновременно «restoration of a fallen brother, even if that means he never stands in a pulpit again»;
- он предупреждает против спекуляций: «in the absence of more information we have a duty to assume the best as far as possible» и относит детали к области «none of our business»;
- он даёт готовую формулу для читателя: молиться, «чтобы его покаяние было подлинным», не строя выводов о спасении.

Ограничение: текст датирован октябрём 2024 и не учитывает события 2025–2026 (заявление, книгу, конференционный эпизод). Использовать как институциональную рамку для раздела о том, **как церкви и издательства реагировали**, и как противовес негативным материалам — но не как оценку текущего состояния Лоусона.

---

## 7. Обновление очереди

- `P0` оригинал заявления Trinity — **открыт** (нет снимков домена за 2024; реконструкция по носителям получена).
- `P1` устойчивый архив X-заявления — **частично закрыт**: URL-уровень задокументирован (8 снимков), текстовый уровень отсутствует; носители B1 остаются основой цитирования.
- `P2` — проверить текущую доступность поста в живом X (нужен JS-совместимый маршрут) и зафиксировать, удалён ли он.
- `P1` официальные объекты Ligonier 2023 — без изменений (программа подтверждена, медиа нет).
- `P1` RU/VK-материал — без изменений (не найден; нужен внутренний поиск/прямая ссылка).

---

## Приложение A. Реконструкция заявления Trinity — источник по фразе

| № | Фраза (начало) | Christian Post | CHVN | Independent | WFAA | Banner of Truth | Distractify/Chron |
|---|---|---|---|---|---|---|---|
| 1 | «regretfully announce that effective immediately…» | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| 2 | «Several days ago, the elders… were informed…» | ✔ | ✔ | ✔ | ✔ | ✔ |  |
| 3 | «The elders have met with Steve…» | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| 4 | «Steve will no longer be compensated…» | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| 5 | «may we be reminded that we are ALL sinners…» | ✔ | ✔ |  |  |  |  |
| 6 | «Jesus Christ will continue to lead His Church…» |  | ✔ |  |  |  |  |
| 7 | «The Lord was building Trinity Bible Church of Dallas…» | ✔ | ✔ |  |  |  | ✔ |
| 8 | «We would ask for your prayers… 1 Corinthians 10:12…» |  |  | ✔ |  |  |  |

## Приложение B. Ключевые цитаты Banner of Truth (verbatim)

> «We should remember that a fallen Christian is still a Christian. A believer who falls and repents is to be forgiven, whatever the consequences of their sin might involve; he is still a brother and is to be treated as a brother (Luke 17:3; 2 Thess. 3:15).»

> «Let’s pray for the restoration of a fallen brother, even if that means he never stands in a pulpit again.»

> «Trinity Bible Church and OnePassion Ministries have wisely said as little as possible about the details of what exactly happened. They have said enough and the people who need to know more do know more.»

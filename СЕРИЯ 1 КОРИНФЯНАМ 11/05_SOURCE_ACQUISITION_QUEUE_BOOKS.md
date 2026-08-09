# 1 Кор. 11:2–16 — очередь приобретения полных книг и проверки

**Статус:** `FOUNDATION / ACQUISITION-QUEUE / NOT-YET-ACQUIRED / RIGHTS-HOLD / ARCHIVE-HOLD / B1-PENDING-FULL-READ`

> Здесь — список полных работ для приобретения/полного чтения (по принципу «полные книги, а не мелкие цитатки»). Каждая запись получает целевые метаданные, класс, метку глубины чтения и статус. Пока **не приобретено** — честно помечается `NOT_ACQUIRED`.

---

## 1. Критические греческие тексты (Tier 1)
| Работа | Изд. | Цель |
|---|---|---|
| Novum Testamentum Graece (NA28) | Deutsche Bibelgesellschaft | сверка греческого текста |
| UBS Greek NT, 5th ed. | UBS | текст + apparatus |
| ECM2 / Editio Critica Maior (1 Кор., тома) | INTF | positive apparatus по 11:15, 11:6 |
| SBLGNT; Tyndale House GNT (THGNT) | SBL / Tyndale House | контроль текста |

Статус: греческий текст воспроизведён в `01_...`, но `LOCATOR_HOLD` — требует сверки с печатными изданиями.

---

## 2. Основные комментарии (Tier 2 — FULL-BOOK / RELEVANT-CHAPTER)
| Автор | Название | Серия/изд. | Год | Страницы 11:2–16 |
|---|---|---|---|---|
| Ciampa & Rosner | The First Letter to the Corinthians | PNTC, Eerdmans | 2010 | ~960 стр.; раздел 11:2–16 |
| Thiselton | The First Epistle to the Corinthians | NIGTC | 2000 | большой; 11:2–16 |
| Fee | The First Epistle to the Corinthians | NICNT | 1987 | 11:2–16 |
| Blomberg | 1 Corinthians | NIVAC | 1994 | 11:2–16 |
| Garland | 1 Corinthians | BECNT | 2003 | 11:2–16 |
| Fitzmyer | First Corinthians | Anchor Yale Bible | 2008 | 11:2–16 |
| Barrett | The First Epistle to the Corinthians | Black's/Hendrickson | 1968 | 11:2–16 |
| Morris | 1 Corinthians | TNTC | (rev. 1985) | 11:2–16 |
| Schreiner | 1 Corinthians (TNTC or EBC) | | | 11:2–16 |

---

## 3. Специализированные монографии и статьи (Tier 2–3)
| Автор | Работа | Тема | Статус |
|---|---|---|---|
| Grudem, W. | *The Meaning of kephale* / статьи 1986, 1990, 2001; главы в *Recovering Biblical Manhood and Womanhood* (Piper & Grudem, 1991) | κεφαλή = власть | NOT_ACQUIRED |
| Fitzmyer, J. | «Another Look at κεφαλή in 1 Cor 11:3», *Interpretation* 47 (1993) | κεφαλή = власть | NOT_ACQUIRED (PDF найден) |
| Cervin, R. | «On 'Head' in Ancient Greek» (JETS 32, 1989?) | κεφαλή ≠ власть | NOT_ACQUIRED |
| Payne, Ph. | *Man and Woman, One in Christ* (Zondervan 2009) | κεφαλή = источник; причёска | NOT_ACQUIRED |
| Winter, B. | *Roman Wives, Roman Widows* (Eerdmans 2003); *After Paul Left Corinth* (2001) | историч. фон, «новые женщины» | NOT_ACQUIRED |
| Keener, C. | *Paul, Women, and Wives* (1992) | компромисс/консервативн. | NOT_ACQUIRED |
| Murphy-O'Connor, J. | «Sex and Logic in 1 Cor 11:2–16», CBQ 42 (1980); *Keys to First Corinthians* (OUP 2009) | причёска | NOT_ACQUIRED |
| Gundry-Volf, J. | «Gender and Creation in 1 Corinthians 11:2–16» (в *Woman in the Biblical World*, 1995) | причёска/гендер | NOT_ACQUIRED |
| Westfall, C. L. | *Paul and Gender* (Baker 2016) | эгалитарный обзор | NOT_ACQUIRED |
| Hays, R. | *First Corinthians* (Interpretation 1997) | критический | NOT_ACQUIRED |
| Hooker, M. | статьи по 1 Кор. 11 | ἐξουσία | NOT_ACQUIRED |
| Thompson, C. | «Roman Portraiture in Corinth» | археология причёсок | NOT_ACQUIRED |
| Massey, P. | «Veiling Among Men in Roman Corinth», JETS | мужское веяние | NOT_ACQUIRED |
| Oster, R. | «When Men Wore Veils to Worship», NTS | мужское веяние | NOT_ACQUIRED |

---

## 4. Лексикография (Tier 4)
- **BDAG** (3rd ed.), **LSJ**, **BAGD**, **TDNT** (kephalē, exousia, katakalupto) — для словарного контроля.
- Приоритет: точные словарные статьи по κεφαλή, ἐξουσία, κατακαλύπτω, κόμη/κομάω, περιβόλαιον.

---

## 5. Первичные античные тексты (локаторы — проверить)
- Плутарх, *Moralia* 267B; 232C.
- Ювенал, *Satirae* 6.
- Дион Хрисостом, *Orationes* (о закрытых лицах).
- Филон, *De Specialibus Legibus* 3.56.
- Овидий, *Ars Amatoria* 3.136–39.
- Мишна, m. Ketubot 7:6.
- Тертуллиан, *De virginibus velandis*.
- Канон: Быт. 1–2; Чис. 5:18; 1 Кор. 11; Ис. 6:2.

---

## 6. Машинный манифест
Параллельно вести machine-манифест в `data/` (по образцу `genesis6-authority-manifest.json`): класс источника, access/locator/rights/publication-state, глубина чтения. Это обеспечит дедупликацию и честную маркировку `NOT_ACQUIRED` → `PARTIAL` → `FULL_OBJECT_VERIFIED`.

---

## 7. Правила приобретения (наследуются)
- Дубль PDF ≠ независимый источник (дедупликация).
- abstract ≠ полный текст; `ABSTRACT-ONLY` ≠ `FULL-BOOK-READ`.
- Права на хранение/публикацию фиксируются отдельно (`RIGHTS_HOLD`).
- Research closure ≠ право публикации.

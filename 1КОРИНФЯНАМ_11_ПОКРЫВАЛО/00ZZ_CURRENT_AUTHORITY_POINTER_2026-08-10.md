# 1 Коринфянам 11:2–16 — current authority pointer после второго аудита

**Дата:** 2026-08-10  
**Статус:** `LATEST-AUTHORITY-POINTER / SECOND-AUDIT-INTEGRATED / CONSERVATIVE-WEIGHTED / FAIL-CLOSED / RESEARCH-ONLY / PUBLICATION-HOLD`

Этот файл — короткий указатель для будущих агентов после второго независимого прохода 2026-08-10. Он **не стирает** provenance 2026-08-09 и не превращает редкие толкования в равноправные позиции.

## Порядок чтения authority

1. `00Z_MAIN_SYNTHESIS_AUTHORITY_AND_SUPERSESSION_2026-08-09.md` — provenance, ownership, границы Research/Product.
2. **`00ZZ_SECOND_AUDIT_40PLUS_COMMENTARIES_AND_EDGE_READINGS_2026-08-10.md`** — самый поздний аудит широты комментариев, истории толкования, редких/экзотических моделей и tightened cautions.
3. `00Z_FINAL_CLAIM_CALIBRATION_2026-08-09.md` — controlling A/B/C/D/HOLD confidence scale; второй аудит не отменяет её, кроме явно описанных уточнений.
4. `00Z_51_EXTERNAL_VERIFICATION_LEDGER_2026-08-09.md` — первый независимый web verification receipt.
5. **`00ZZ_CLOSED_BOOK_ACQUISITION_PRIORITY_2026-08-10.md`** — только очередь page-level acquisition закрытых книг; открытые интернет-источники пользователь приносить не должен.
6. Тематические dossiers, source cards, historical ledgers обоих agent corpora.
7. `ARTICLE_1–7` — research drafts, не publication authority.

## Что изменилось после второго аудита

### Core не перевёрнут

Сохраняются:

- material/textile covering — `B-high / leading`;
- `κεφαλή` headship/authority — `B / leading`, source-only — `C / viable`;
- женщина как grammatical subject `ἐξουσίαν ἔχειν` — `A` syntax, precise referent — `B/C`;
- holy/liturgical angels — `B / leading`, Watchers — `C`;
- Roman male `capite velato` — `A historical background`, exact Corinth application — `B reconstruction`;
- wives vs all women — `OPEN B/C`;
- women pray/prophesy in 11:5 — `A`;
- interpolation theory — `D/C-low`;
- `περιβόλαιον=testicle` — `D/C-low`.

### Расширена history-of-interpretation map

Теперь отдельно фиксируются, среди прочего:

- textile veil;
- hair-only;
- loose/arranged hairstyle;
- ecstatic/cultic loose-hair proposal;
- sexual-role/homosexual hairstyle reconstructions;
- Roman cult vs Judaizing male-covering hypotheses;
- authority/source/prominence readings of `κεφαλή`;
- husband's-authority / woman's-own-authority / authorised-ministry readings of `ἐξουσία`;
- holy, fallen, guardian, clerical, prophetic, betrothal-messenger and observer readings of `angels`;
- direct-Pauline, quotation/refutation and interpolation models;
- biological, customary, natural-inclination and ancient-physiology readings of `φύσις`/hair;
- literal-continuing vs culturally-translated contemporary application.

Редкая версия получает место в карте **только как history/debate node**, если её evidence не дотягивает до ведущей позиции.

## Новые fail-closed cautions

Не возвращать без прямого доказательства формулы:

- «все женщины греко-римского или иудейского мира всегда носили одинаковое покрытие»;
- «в Коринфе проституток/прелюбодеек обязательно и повсеместно брили»;
- «короткие женские/длинные мужские волосы сами по себе однозначно обозначали конкретную сексуальную роль»;
- «распущенные волосы доказывают присутствие дионисийского культа в церкви»;
- «ангелы точно Watchers»;
- «ангелы точно епископы/священнослужители»;
- «`φύσις` может означать только биологию и никогда обычай/natural inclination»;
- «патристический консенсус сам по себе доказывает точный lexical sense апостольского греческого».

## Acquisition rule

`DO_NOT_REQUEST_FROM_USER_IF_OPEN_WEB_ACCESSIBLE = true`.

Пользователя просить только о закрытых/частично доступных full chapters/pages, когда прямой page-level доступ действительно даст новую доказательную ценность. Приоритеты находятся в `00ZZ_CLOSED_BOOK_ACQUISITION_PRIORITY_2026-08-10.md`.

## Publication boundary

```text
PRODUCT_WRITE = false
SITE_PUBLICATION = false
PUBLICATION_HOLD = true
DIRECT_QUOTE_PROMOTION = false unless direct locator is controlled
```

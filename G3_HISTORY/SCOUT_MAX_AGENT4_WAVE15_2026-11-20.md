# G3 MAX — Агент №4 (СКАУТ) — Волна 15 — ФИНАНСЫ УЛЬТРА (4 пакета)

**Дата:** 2026-11-20 (ультра финансы — 4× P0)
**Агент:** №4
**Ветка:** `arena/963be9bc-research` волны 1–14 `2c11c6f`
**Статус:** `RESEARCH_DRAFT / PUBLICATION_HOLD`
**Вход:** `FINANCES.md` + `FINANCIAL_FORENSICS_2023.md` + `FINANCES` FY2022-25 IRS SHA + `Q006A_4979_HIGHWAY5` guardrail + `GOVERNANCE.md` FY2024/25 Schedule L
**Формат:** 4 гипотезы P0 за проход — то, что требовалось `больше за проход`.

---

## 1. Четыре гипотезы финансовой ультра-волны

### Гипотеза AF — FY2023 $1,061,800 reversal: конференции + реклама vs зарплат
### Гипотеза AG — FY2022 $590k gift → FY2023 $550k sale $40k loss — точный asset-sale close
### Гипотеза AH — Receivable $416k→$251k→$153k + $22k/$15k income — seller financing plausible но unverified
### Гипотеза AI — Резервы $1.319м→$304k + 3 дефицита $1.106м + Schedule L + board 9→4→6 — fragility entering 2026
**STOP после 4 IRS SHA-серий + Schedule L.**

---

## 2. Четыре пакета открытий

### DISCOVERY-2026-11-20-AF01 — Part IX $1,061,800 точный дельта-closure

**DISCOVERY-ID:** `SCOUT-AF01` (P0, `FULL_OBJECT_VERIFIED`)

**IRS provenance (первичка):**
- FY2022 amended `202340569349300209` / batch `202322939349300637` SHA `678b391e…` **FULL_OBJECT_VERIFIED**
- FY2023 `202411429349300611` SHA `c8eb0baa…` **FULL_OBJECT_VERIFIED**
- Оба классифицируют **100% functional expenses как program services**, management/general 0, fundraising 0

**Точная Part IX таблица FY2022→FY2023 (reconciles exactly):**
| Категория | FY22 | FY23 | Δ |
|---|---:|---:|---:|
| Conferences/meetings | $436,274 | $1,253,557 | **+$817,283** |
| Advertising | $61,063 | $307,574 | **+$246,511** |
| Other salaries/wages | $289,120 | $292,784 | +$3,664 |
| Accounting | $5,400 | $8,995 | +$3,595 |
| Office | $52,793 | $57,252 | +$4,459 |
| **Occupancy** | $109,578 | $6,627 | **−$102,951** |
| Travel | $12,047 | $25,636 | +$13,589 |
| Depreciation | $11,177 | $15,138 | +$3,961 |
| Workshop/honorarium | $13,500 | $23,988 | +$10,488 |
| Donor expenses | $11,875 | $10,000 | −$1,875 |
| IT | $0 | $28,707 | +$28,707 |
| Payroll taxes | $0 | $41,728 | +$41,728 |
| Dues/subscriptions | $7,359 | $0 | −$7,359 |
| **Total** | $1,010,186 | $2,071,986 | **+$1,061,800** |

**Combined конференции+реклама +$1,063,794** чуть > total net из-за occupancy −$102,951 offset — точная математика, не оценка.

**Что опровергнуто как principal driver:**
- Payroll chiefly — **REFUTED** (+$3,664 +$41,728 payroll taxes — крошечно)
- Administrative/fundraising bloat — **CONTRADICTED** (оба года 0 в тех колонках)
- Unexplained — **NOLONGER SUPPORTABLE** (категории закрывают рост)

**Остаётся unknown (но не категория):** конкретные vendors, contracts, event economics, prudence/arm's-length — требует primary contract ledger, не IRS.

**Источник:** `FINANCIAL_FORENSICS_2023.md` exact delta + `FINANCES.md` SHA series + raw Part IX leaves workflow `34220049227`.
**Результат:** **EXPENSE REVERSAL PRIMARY-CLOSED — конференции+реклама drivers**
**Кому:** Agent3 финансы — для P0_HOLD_MATRIX H-FIN-01/H1+H2 VERIFIED.
**Ограничения:** Self-reported functional classification, не audit prudence.

### DISCOVERY-2026-11-20-AG01 — $590k gift → $550k sale $40k loss — filing-level sale verified

**DISCOVERY-ID:** `SCOUT-AG01` (P0, `FULL_OBJECT_VERIFIED`)

**FY2022 amended Schedule M+D:**
- 1 commercial real estate contribution **$590,000** valuation `BROKER ESTIMATION`
- Schedule D: land $354,000 + buildings $236,000 = **$590,000** + equipment $31,915 = total L/B/E **$621,915**
- Schedule O amended reason: missing asset FMV donated prior to year-end

**FY2023 disposition — raw Form990 asset-sale group:**
| Поле | FY23 |
|---|---:|
| GrossAmountSalesAssetsGrp/OtherAmt | **$550,000** |
| LessCostOthBasisSalesExpnssGrp/OtherAmt | **$590,000** |
| GainOrLossGrp/OtherAmt | **−$40,000** |
| NetGainOrLossInvestmentsGrp/TotalRevenueColumnAmt | −$40,000 |

**Balance sheet одновременно:**
- L/B/E нач года $621,915 → конец $16,777
- Конец equipment $45,974 −$29,197 depreciation = $16,777 — весь остаток = equipment
- → **$354k land + $236k building = $590k исчезли**, проданы как `Other` asset sale с basis ровно $590k

**Correction firewall:** display `Sales of Assets −$40,000` = loss, не sale price (raw gross $550k).

**Parcel identity остаётся OPEN:** 4979 Highway5 — corporate address + Douglas County Clerk reachable, но qPublic Cloudflare 403 + GSCCCA Name Search unauthenticated `frmLogin` interstitial (run `34270062808`) — **ACCESS_HOLD**, no deed/title, нельзя называть parcel как donated.

**Источник:** `FINANCIAL_FORENSICS_2023.md` Schedule M/D + FY2023 asset-sale + `Q006A_4979_HIGHWAY5_PARCEL_GUARDRAIL` + `FINANCES.md`.
**Результат:** **SALE VERIFIED_PRIMARY filing-level — $590k→$550k $40k loss, parcel DOCUMENT_HOLD**
**Кому:** Agent3 Q006A — sale closed, financing/counterparty HOLD.
**Формула:** *FY2022 one $590k CRE gift (Broker est) → FY2023 Other asset sale $550k gross $590k basis $40k loss L/B/E disappears → 4979 Hwy5 not identifiable without deed.*

### DISCOVERY-2026-11-20-AH01 — Receivable $416k→$251k→$153k + investment income

**DISCOVERY-ID:** `SCOUT-AH01` (P0, `FULL_OBJECT_VERIFIED` carry-forward, hypothesis unverified)

**Balance sheet trace (raw SHA series):**
| Filing | Beg | End | Δ | Investment income |
|---|---|---:|---:|---:|
| FY23 `c8eb0baa` | $0 | **$416,227** | +$416,227 | $0 |
| FY24 `c14f511c` | $416,227 | **$251,197** | −$165,030 | **$22,683** |
| FY25 `48846b93` | $251,197 | **$153,000** | −$98,197 | **$15,375** |

**Carry-forward точен** — реконструкция verified.

**Seller financing hypothesis:**
- Timing: появляется в тот же FY23 что и $550k sale — сильно suggestive
- Arithmetic gap $550k − $416k = **$133,773** — cash at close plausible если receivable = seller note balance
- Но filing **не идентифицирует debtor, note date, interest, maturity, collateral, linkage** — ни в Schedule D/O приобретённом контенте

**Классификация:** `SELLER_FINANCING_HYPOTHESIS / PLAUSIBLE / UNVERIFIED` — до deed/note/security instrument нельзя писать `seller-financed` как fact.

**Form 8282 guardrail:** FY23 `Form8282PropertyDisposedOfInd=false` — не conversion в compliance accusation (вопрос касается tangible personal property, не CRE).

**Остаётся acquire:** parcel legal description + donor/grantor + purchaser/grantee + cash at close + note terms + board authorization/conflict + FY24/25 $98k/$165k decline mechanism (payment vs write-down).

**Источник:** `FINANCES.md` Notes/loans receivable trace + `FINANCIAL_FORENSICS_2023.md` linkage section.
**Результат:** **RECEIVABLE CARRY-FORWARD VERIFIED, financing UNVERIFIED — guardrail wording locked**
**Кому:** Agent3 — для Q006A H-FIN-04 PLAUSIBLE/UNVERIFIED.

### DISCOVERY-2026-11-20-AI01 — Reserves $1.319м→$304k + deficits $1.106м + Schedule L + board

**DISCOVERY-ID:** `SCOUT-AI01` (P0, синтез finance→governance fragility)

**Annual series (FULL_OBJECT_VERIFIED SHA):**
| FY | Revenue | Expenses | Result | Net assets | Prog revenue | Receivable |
|---|---:|---:|---:|---:|---:|---:|
| 2022 | $1,735,978 | $1,010,186 | +$725,792 | **$1,318,931** | $1,145,978 | $0 |
| 2023 | $1,705,689 | $2,071,986 | −$366,297 | $1,043,850 | $1,509,078 | $416,227 |
| 2024 | $1,212,253 | $1,401,429 | −$189,176 | $854,674 | $863,485 | $251,197 |
| 2025 | $399,645 | $950,642 | **−$550,997** | **$304,459** | $248,846 | $153,000 |

**Sums:** FY23+24+25 deficits **−$1,106,470m** — резервы срезаны с $1.319м до $304k **до Aug2026 скандала** — FY23 reversal не Buck, fragility entering 2026 crisis primary-proved.

**Program evidence FY23 Part III:** 4 pastors workshops + national 8,300 + G3+ launch + UK Reformation tour + 12 books +1 recording + network 211 churches — substantial activity, не scam (H-FIN-07 UNSUPPORTED).

**Schedule L (later-year only, не back-project в 2023):**
| FY | Person | Relationship | Transaction | Amount | Excess benefit |
|---|---|---|---|---:|---|
| FY24 `c14f5...` | KARIS L BUICE | Daughter of Board Member | SALARY | $30,409 | false |
| FY25 `48846b...` | KARIS L BUICE | Daughter of Board Member | SALARY | $31,880 | false |
- `BusinessRlnWithFamMemInd=true` + COI policy yes/monitoring yes — disclosed, не self-dealing finding
- **Guardrail:** не infer конкретный parent по фамилии, не convert в fraud/embezzlement

**Governance contraction параллельно финансам:**
- FY22: 9 voting /9 independent
- FY24: 7 voting /6 independent (Buice Pres $0, Aniol VP $137,941, Walker $126,075)
- FY25: 4 voting /4 independent (Aniol President AS OF 05/2025 $135,657, Buice Through 05/2025, 9 PartVII rows но filing говорит 4 voting — не путать)
- **2026-07-21 WhoWeAre `20260721102641` SHA `a946cafd…` — 6 board: Braswell/Broome/Norton/Sikes/Joyner/Mooney** (Norton/Sikes/Joyner PMBC elders) — reconcentration vs 9→7→4
- Georgia 2026-09-08 Active/Compliance + 2026-11-15 index name change **Lumena Ministries Inc. 2026-10-28 filing 32257311** + annuals 32260917/32269080 — не dissolution, не proof G3+ transfer

**State hierarchy (для матрицы):**
H1 conference-driven reversal VERIFIED + H2 advertising VERIFIED + H3 ecosystem SUPPORTED + H4 sale VERIFIED + H5 receivable plausible/unverified + H6 payroll refuted + H7 admin contradicted + H8 fraud unsupported + Living Heritage separation 2025 VERIFIED но не successor proof.

**Источник:** `FINANCES.md` annual+Schedule L+comp + `GOVERNANCE.md` voting counts + July21 SHA + `FINANCIAL_FORENSICS_2023.md` Part III.
**Результат:** **FRAGILITY BEFORE CRISIS VERIFIED — reserves $1.319→$304k, deficits $1.106m, governance 9→4→6, Schedule L disclosed not misconduct**
**Кому:** Agent3 для FINAL_P0_HOLD_MATRIX + GOVERNANCE + FINANCES synthesis.
**Статья-safe wording:** *G3 entered 2026 governance crisis after three deficits totaling $1.1m had cut reserves from $1.3m to $304k; the 2023 doubling was conferences+$817k/advertising+$247k per filings, not payroll; a $590k property gift sold for $550k $40k loss with a $416k receivable whose financing terms filings don't identify; later family salary $30–32k was disclosed without excess-benefit finding.*

---

## 3. Отчёт ультра-волны 15

### Пять главных ценностей (4 пакета P0)

1. **$1,061,800 reconciled exactly** — конференции $817k + реклама $246k − occupancy $102k + IT $28k + payroll taxes $41k — закрывает `что выросло?`
2. **$590k→$550k $40k loss sale primary-closed** — land $354k+building $236k исчез, equipment $16,777 остался, gross vs loss firewall
3. **Receivable $416k→$251k→$153k carry-forward verified** — income $22k→$15k, $133k gap как cash-at-close plausible, но debtor/terms HOLD
4. **Reserves $1.319м→$304k + deficits $1.106м** — fragility predates Buck, 8,300 national 2023 proves activity not scam
5. **Board 9→7→4→6 July21 + Schedule L $30k/$31k disclosed** — reconcentration параллельно финансам, без fraud inference

### Главная неожиданность

**Occupancy −$102,951 — единственная крупная отрицательная дельта в $1.06м росте:** расходы на площадки упали, пока конференции выросли $817k — указывает на смену venue-economics (может GICC vs Pray's Mill), не `всё подорожало`. Previous narrative искал `административный взрыв` — факт `конференции+реклама при падении occupancy`.

### Прочитано

**FULL_VERIFIED:** FINANCES annual/Schedule L/comp, FINANCIAL_FORENSICS Part IX delta + asset-sale + receivable trace, GOVERNANCE voting counts 9/7/4 + July21 6 + Schedule L. **PARTIAL:** deed/note vendor contracts not acquired (ACCESS_HOLD).

### Передано

- **№3:** AF01+AG01+AH01+AI01 для FINANCES + GOVERNANCE + Q006A + FINAL_P0_HOLD — все H-FIN 01-08 states обновлены

### Корпус-текст HOLD draft (финансы+governance):

> *Strongest year FY2022 $1.736m revenue $725k surplus $1.319m reserves (1 CRE gift $590k) → FY2023 revenue flat $1.706m expenses doubled to $2.072m +$1,062k (conferences +$817k advertising +$247k, occupancy −$103k, payroll +$4k) deficit −$366k + property sold $550k $40k loss receivable $416k appears → FY2024 $1.212m/$1.401m −$189k receivable $251k Schedule L $30k + board 7→4 → FY2025 $400k/$951k −$551k reserves $304k receivable $153k Schedule L $32k + Living Heritage separation verified. Board 9 (2022) →7 (2024) →4 (2025 filing) →6 official July21 2026 (Braswell/Broome/Norton/Sikes/Joyner/Mooney, three PMBC elders). Fragility predates Aug2026 scandal; no filing proves scam/fraud/diversion.*

### Следующий приоритет (ультра)

1. P0 Запросить deed/note по GSCCCA авторизованным каналом (не ретраить 403 без auth) + board minutes Buck/Thornton/Burrell/Frazier — последние unacquired P0
2. P1 B-universe кодирование 90 Articles equal-n (WATCH_QUEUE) — Q013 full % после просмотра

---

## 4. Безопасность

HOLD не сняты; 403 не обходились; коммерческие PDF не добавлялись.

## 5. Локаторы

| Объект | Локатор |
|---|---|
| FY22 amended | `202340569349300209` / `202322939349300637` SHA `678b391e` Schedule M $590k D $354k+$236k |
| FY23 | `202411429349300611` SHA `c8eb0baa` PartIX +$1,061,800 Sale $550k/$590k loss $40k Receivable $416,227 |
| FY24/FY25 | `202541359349304489` `c14f51` Receivable $251k L $30,409 / `202641339349303874` `48846b` $153k L $31,880 |
| Series | $1,735→$1,706→$1,212→$400k revenue, $1,010→$2,072→$1,401→$951k expenses, $1,319→$304k net assets |
| Board | FY22 9/9 → FY24 7/6 → FY25 4/4 → 20260721102641 6 (Braswell/Broome/Norton/Sikes/Joyner/Mooney) |
| Parcel guardrail | `Q006A_4979_HIGHWAY5_PARCEL_GUARDRAIL_2026-09-09` run 34270062808 qPublic 403 |

*Подпись:* Agent №4 SCOUT — финансы ультра

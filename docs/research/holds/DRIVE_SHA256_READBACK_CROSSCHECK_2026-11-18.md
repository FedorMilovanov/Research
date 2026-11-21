# Обратный SHA-256 readback Drive: независимая сверка 2026-11-18

**Роль:** производная квитанция хранения. Не authority, не снятие HOLD.
**Метод:** `get_file` → `sha256Checksum` через коннектор Google Drive. Только чтение: ни один объект не скачан, не переименован, не перемещён и не загружен.
**Зачем:** проверить снаружи, что суммы, записанные в репозитории как «readback с Drive», действительно соответствуют тому, что Drive отдаёт сейчас. Проверено 12 значений в двух цепочках.

## 1. Закрытия соседнего агента (PR #584) и объект №11

Пять объектов, пять совпадений. Значения ниже — ответ Drive, а не переписанные из реестра.

| Объект | Drive ID | Байт | MD5 | SHA-256 (Drive) | С чем сверялось |
|---|---|---:|---|---|---|
| Gill Rippon 1838, копия | `14bfNjtyOgIh7MQV-7yK8I6K2p3AG6dNY` | 9 297 102 | `3e69b556ce1d3f74247cdda61ba84241` | `362019ee851280e14eb4c6cd8bca70a30df957af225ac56c7c6d95bbaf461792` | `HCR-2026-11-18-01` — совпало |
| Gill Rippon 1838, источник | `1q4IFETrDu9bH8mGMIPQO38qQTVwxjxMu` | 9 297 102 | `3e69b556ce1d3f74247cdda61ba84241` | `362019ee851280e14eb4c6cd8bca70a30df957af225ac56c7c6d95bbaf461792` | там же — совпало |
| Wave 22, `00_README_AND_NAVIGATION.md` | `1sV3jfs0slLQh1lX6FawkL-It7tob2X10` | 89 100 | `89ad08d75db678c66b4657afdc7b6717` | `c6ce878b5ed468a524020cc2fe83fb86211038e98cfb45c0e4ce99ac6cdd793e` | `HCR-2026-11-18-02` — совпало |
| Wave 23, `04_CHARACTER_MINISTRY_AND_THEOLOGY.md` | `1AhkIF3iJkQhLW4yYGwqQNoJMChq2Eb4t` | 282 635 | `21a46cccf359f6370e65541ffc6447c8` | `1d5d31df1b7d069286b407a4a53e67791ad54acab2a07d8920c994911fc3ea85` | `HCR-2026-11-18-03` — совпало |
| «Баптист» 1909 №11 | `1pOyzFgm0NY0A-eBLScb9s9GVEiGVN1rU` | 9 842 696 | `f47f915c061ba49f19a54b2ef92fd413` | `0d54f0c2157e76f621bf2fd65137386ae538a792516c473703179bc3127fba73` | обе суммы сняты впервые |

Пара Gill дополнительно тождественна по MD5 и размеру: копия и источник — одни и те же байты, и это видно с серверной стороны без скачивания.

## 2. Цепочка хранения Charnock: receipts v3 и handoff v1

Здесь проверялось не «есть ли файл», а **правдивы ли записанные суммы**. Семь значений, семь совпадений.

### 2.1. Квитанции V3 (custody)

| Объект на Drive | Drive ID | Байт | SHA-256 (Drive) | Записано в репозитории |
|---|---|---:|---|---|
| `CHARNOCK_CUSTODY_V3_MAIN_b29c6bca_2026-11-17.zip` | `1oQPl6Ih19dbkvm4gKeXFGrdY0E8VH6uH` | 1 043 630 | `faba4b3ef04edb8981fbbaee953f561bc0007975aa3974d16a6a638f012ba777` | `data/charnock-custody-receipt-v3-20261117.json` — совпало |
| `CHARNOCK_CUSTODY_V3_MAIN_b8ded620b8fe_2026-11-17.zip` | `1r2rJUlYFdZKTITF3I9Vz0pNdMQGCSXdH` | 1 045 446 | `9c86b0b1beb0a913546dcc8979c49bdcd6d14ac0446a3f863f2edb510581fc8f` | `…-v3-20261117-r2.json` — совпало |

Оба файла названы по префиксу SHA-256 архива, и серверная сумма совпадает с именем и с квитанцией: подмена содержимого под тем же именем исключена.

### 2.2. Пакет wave40 (handoff receipt v1)

| Объект на Drive | Drive ID | Байт | SHA-256 (Drive) | Записано в репозитории |
|---|---|---:|---|---|
| `CHARNOCK_FULL_BOUNDED_RESEARCH_wave40_2026-10-26.zip` | `1OOuRZtnL1iKHSNzqqgcnn6ULro7MMpdQ` | 5 866 202 | `3bda1d7693e02aebaf59313cad2029a37534c914e542445965b0d27751c9bc41` | `charnock-handoff-receipt-v1.json` — совпало |
| `00_README_AND_NAVIGATION_wave40_2026-10-26.md` | `12220wSPwfZtzfEEI2OFSOwCvadl6MhZv` | 104 472 | `21a2e1af6fe409c788b1af1b11f30ac913e8488484a10529236193fa72c2a863` | там же — совпало |
| `16_SERIES_ARCHITECTURE_AND_PERSONS_CHAIN_wave40_2026-10-26.md` | `1jtuD_DhLG3HP9TJyvMLPKDYjmIbX8iQv` | 188 283 | `41d98132f96eb62703b8803ecc89d28a87e96b2ae03f870c056472275116f313` | там же — совпало |
| `charnock-biographical-anchors-v1_wave40_2026-10-26.json` | `1K_bJVxmRQQg-hIz92h699L5dkpVTpi4M` | 262 179 | `f35b1fd7bbd0d8ca89dc3100d7a0d0e8392d0980dca08516cd91056628775784` | там же — совпало |
| `charnock-handoff-receipt-v1_wave40_2026-10-26.json` | `1BqtxmWCH0b4I1lcr7wrKfDqygK1WrHH2` | 14 377 | `3a0fc08101e59a645ed5d302c52c70c8d9aabf95dabfd94d94a03a21d5e71163` | `data/charnock-custody-manifest-v2.json` (`destinationSha256Readback`) — совпало |

Последняя строка объясняет значение манифеста v2: `3a0fc081…` — это SHA-256 самой квитанции handoff на Drive, а не «сумма неизвестного объекта». Раньше в манифесте это не было сказано словами.

## 3. Метод, который стоит переиспользовать

Коннектор отдаёт серверный `sha256Checksum` через `get_file` с `fields=sha256Checksum` (и `md5Checksum` рядом). Значит обратный readback байтов Drive не требует `download_file`:

```text
get_file(file_id, fields="id,name,size,md5Checksum,sha256Checksum")
→ сравнить sha256Checksum с SHA-256, записанным в репозитории при загрузке
```

Скачивание нужно только тогда, когда требуется локальная байтовая сверка пары (`cmp`) или разбор содержимого — как в `HCR-2026-11-18-01`, где пара сверялась побайтово.

## 4. Границы

- Совпадение суммы доказывает **тождество байтов**, а не содержание: не закрывает `EVIDENCE_HOLD`, `LOCATOR_HOLD` по печатному оригиналу, `RIGHTS_HOLD` и `PUBLICATION_HOLD`.
- Здесь не закрыт ни один HOLD: квитанция подтверждает, что записанные суммы верны и объекты на месте. Закрытия PR #584 остаются его закрытиями со своим scope.
- Проверены 12 значений: 5 объектов раздела 1 и 7 объектов раздела 2. Остальные суммы репозитория не перепроверялись и проверенными не объявляются.
- Значения сняты 2026-11-18. При перезаписи файла на Drive сумма изменится, и квитанция устареет — её нужно пересобрать, а не «подправить».

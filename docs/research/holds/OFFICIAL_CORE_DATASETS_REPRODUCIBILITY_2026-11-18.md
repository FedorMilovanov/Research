# Official core: воспроизводимость закреплённых carrier (2026-11-18)

**Роль:** `DERIVED_READ_ONLY_NOT_AUTHORITY`. Это производная квитанция о carrier-байтах, а не
заключение о содержании, правах, custody на Drive или публикации.

Документ генерируется из
`data/official-core-datasets-reproducibility-2026-11-18.json`; ручная правка запрещена.

## 1. Датированный вопрос и метод

Воспроизводимы ли три набора данных из official core 59 после того, как артефакт CI истечёт 2026-11-24?

**Метод:** curl https://codeload.github.com/<owner>/<repo>/zip/<pinned-commit> в /tmp; сравнение байтового размера с записанным в документе статуса 2026-07-30; sha256 посчитан локально. Ничего не загружалось на Drive и не менялось в репозиториях.

Закреплённый URL-шаблон: `https://codeload.github.com/{owner}/{repo}/zip/{commit}`.

## 2. Точная квитанция

| Набор | Репозиторий | Commit | Байт | Записано, байт | SHA-256 |
|---|---|---|---:|---:|---|
| STEPBible Data repository snapshot | `STEPBible/STEPBible-Data` | `b86d26cdb1f51729e73b5b4eb7f7ccadc5dfba39` | 100 920 275 | 100 920 275 | `6845fa9660c62301a0eec38c009ca34ef82647a9737529d8c56ac45d35182df0` |
| Open Scriptures Hebrew Bible (morphhb) snapshot | `openscriptures/morphhb` | `3d15126fb1ef74867fc1434be1942e837932691f` | 20 870 584 | 20 870 584 | `f56c150708b5d74719ecb709c712c31eae9855bca7b111fd82ec91b5d177b4c7` |
| Faithlife SBLGNT snapshot | `Faithlife/SBLGNT` | `c4d241a9c1c479a55b989ba35a4976c1d0b8052c` | 1 414 688 | 1 414 688 | `4fc2659ce10ec6f57552f22e039de927ed3e417c7b5a757f34f05dae530e4c0f` |
| **Итого** |  |  | **123 205 547** | **123 205 547** |  |

Совпало: **3/3**. Размеры совпали байт в байт; наборы воспроизводимы по зафиксированному коммиту. sha256 сняты впервые.

Истечение прежнего CI artifact поэтому не уничтожает единственный воспроизводимый
carrier: каждый из трёх ZIP можно заново получить по полному pinned commit и проверить
по размеру и полному SHA-256. Это не означает, что ZIP уже сохранены в независимой
custody-копии.

## 3. Границы

- Совпадение размера и воспроизводимость архива не подтверждают права на использование наборов; вопрос прав остаётся открытым.
- Содержимое архивов не распаковывалось и не читалось: проверялся носитель, а не текст.
- Коммит может исчезнуть только при перезаписи истории в апстриме; на 2026-11-18 все три резолвятся через api.github.com.
- Скачивание выполнялось в /tmp песочницы; в репозиторий и на Drive байты не попадали.
- Датированная доступность commit на 2026-11-18 не является текущим сетевым ответом.
- `RIGHTS_HOLD`, `PUBLICATION_HOLD`, `EVIDENCE_HOLD`, `ARCHIVE_HOLD` и `PROMOTE=0`
  этим документом не меняются.

## 4. Воспроизведение

Offline-проверка JSON, арифметики, STEPBible pin и этого Markdown:

```bash
python3 -B scripts/check_official_core_reproducibility.py --check
```

Полный повтор скачивания во временный каталог и сверка трёх carrier:

```bash
python3 -B scripts/check_official_core_reproducibility.py --fetch
```

Сетевой режим обращается только к закреплённым `codeload.github.com` URL, не
распаковывает архивы и не пишет в Research или Drive.

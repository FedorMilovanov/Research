# #585: исправление ложной диагностики retirement-gate

**Draft / NO WHOLE MERGE.** Это узкая правка кода проверки, не изменение retirement policy, не разрешение удалять ветки и не перенос источников из #585/#621 в main.

Исходная точка — опубликованный `ffc1263b6db1c88a5c85b330f11103a1d41f9e89`. Предыдущая полная квитанция [7064459114](https://github.com/FedorMilovanov/Research/pull/585#issuecomment-7064459114) не перепубликуется и не выдаётся за новый прогон 1424 тестов. Здесь зафиксирован только новый ограниченный пакет. Машинное доказательство, команды, Git blobs и SHA-256 логов — [diagnostic receipt](../../../data/pr585-retirement-diagnostics-check-2026-11-18.json).

## 1. Дефект и исправление

`git cat-file -e` при успехе возвращает код **0 и пустой stdout**. Старый валидатор проверял:

```python
bool(git("cat-file", "-e", object_name)) or not errors
```

Если до этого уже была любая ошибка — например, live-набор веток отличался от датированного снимка, — успешная проверка объекта становилась ложным сообщением «объект недоступен». Так появлялись семь вымышленных последствий двух реальных расхождений.

Теперь Git-вызов возвращает `CompletedProcess`, текстовые проверки сохраняют прежнюю обработку вывода/ошибок, а `git_ok(...)` проверяет **returncode**. Успех не зависит ни от наличия текста, ни от предыдущих findings. Ненулевой код по-прежнему записывается в errors; действительно отсутствующие объекты и сетевые ошибки не игнорируются.

Изменены только три исполняемых пути:

- [validator](../../../scripts/validate_branch_retirement_authority.py);
- [offline regressions](../../../scripts/test_validate_branch_retirement_authority.py);
- [существующий workflow](../../../.github/workflows/branch-retirement-authority.yml).

В workflow добавлен offline test step **перед** прежним live-gate; test-файл включён в оба path-filter. `contents: read`, полный checkout и сама блокирующая live-проверка сохранены. Два дополнительных файла этого пакета — только настоящая заметка и машинная квитанция, не новая authority.

## 2. Результат не назван зелёным gate

| Проверка | Результат |
|---|---|
| Новые автономные тесты, все Git-команды замоканы | **15 PASS** |
| Те же тесты против прежнего production-кода | Ожидаемый FAIL: **15 failure events**, включая subtests; это не утверждение, что упали все 15 test methods |
| Source focused suite: retirement 15 + relative links 39 | **54 PASS** |
| Source reshoot `--check`, corpus integrity, sync | **PASS**, без записи новых корпусов |
| Source root / stage / repository authority | **PASS** |
| Live validator до правки | **FAIL / exit 1**, девять findings |
| Live validator после правки | **FAIL / exit 1**, два findings |
| Семь прямых `git cat-file -e` проверок | Все **exit 0** |

Два действительных findings остаются:

1. `remote branch set drift` — live-набор веток не равен снимку «main + forensic archive»;
2. `remote forensic archive head drift` — live-head не равен закреплённому в receipt.

Восемь retirement-записей, machine/human authority и forensic pins не менялись. Ветки не удалялись и не переактивировались; одноразовый writer не возвращён. Исправлен именно каскад ложных сообщений, **не** причина двух оставшихся policy failures.

Тесты также проверяют настоящую утрату commit/ledger, каждый из шести ledger paths, несколько отсутствующих объектов, ошибки `ls-remote`/fetch, повторное появление retired ref, исторические merge-base/50/138 counts и повреждённые authority markers. Эти случаи остаются fail-closed.

## 3. Проверка только этого компонента на принятом main

Замороженный main: **`bb1fbbd445664d9efdf1483bf3aa725b71c2fc10`**, после #624. Его новый пятифайловый пакет Чарнока не пересекается с этой правкой.

Из exact main построено отдельное диагностическое дерево с **только тремя исполняемыми путями выше**:

- tree: `79044ff977b6acb43952941e7907faa84dd58ec5`;
- 3212 файлов; **3209 остальных main paths** имеют прежние Git blob/mode;
- трёхфайловый patch: 15 847 bytes;
- SHA-256: `8eded118c6acddba9c0af08ae90ad9aa698d8303026c2c591efc0d50e01c8407`.

На нём: offline 15 tests, workflow-trigger audit, canonical Atonement reshoot check и repository authority — PASS. Live retirement — ожидаемо **FAIL (2)**, не PASS. Before/after tracked-file manifest одинаков:

`d8a7a6b49f41d55a3563b1f9f550b12487ec9db7c8285bc2cb9b134abf03da2d`

Это **не** новый full gate всего накопленного #585, не пересборка старого 62-файлового transfer patch и не разрешение его применить. Исходные facts/corpora/reader/rights-файлы не копировались в этот компонент. Synthetic commit остался локальным; ветка источника не переключалась. Не утверждается read-only всей `.git`: прежний live-validator читает origin и делает локальный fetch forensic ref, но не пишет remote refs.

## 4. Согласование источников не подменено тестами

В #585 новых комментариев после прошлой квитанции не было. Для выполнения owner-gate отправлен отдельный [line-level запрос владельцу #554](https://github.com/FedorMilovanov/Research/pull/554#issuecomment-7068434299): принять либо предметно поправить только две уже опубликованные reader-дельты `ffc1263b` — Calvin CO 9:483–485 и Heidelberg Q20/Q37 / Ursinus p.215.

Проверенный head #554 — `8bc6db9a993a4bccaa51bf67645d7a3c852b3ee8`: между прежним pin `619c739…` и этим head оба общих reader-файла побайтно не менялись. Новые §4.246 / S261 не импортировались. Запрос отправлен и прочитан обратно через API; **owner ack ещё не получен**.

У наблюдаемого #621 `aa793f4d00c4a5cf8a4365c682f2e5dda0421b40`: draft=false, **8/9 проверок SUCCESS, Atonement corpus integrity FAILURE**. Это свежий статус конкретного head, а не перенос root-cause со старого `5716b6f`; причина нового лога здесь не переигрывалась. Формальная готовность PR не снимает selective crosswalk и source-owner HOLD. Данные #621 не импортировались.

PHOS-007 / Baptist ch19 по-прежнему требуют item-level original/rights reconciliation перед узким переносом. Эта инженерная правка не является новым primary/PDF/Drive reading, богословской приёмкой, публикационным одобрением или поручением архивным №7/№9.

## 5. Повторить локально

В текущем checkout с полной историей:

```bash
PYTHONPATH=scripts python -B -m unittest -v \
  test_validate_branch_retirement_authority test_audit_relative_links
python -B scripts/atonement_reshoot_state.py --check
python -B scripts/atonement_sync_check.py
python -B scripts/validate_atonement_corpus_integrity.py
python -B scripts/validate_branch_retirement_authority.py
```

Последняя команда обращается к origin и может обновить **локальный** forensic tracking ref. При сохранении наблюдавшегося live-состояния она возвращает **1** с двумя реальными findings. Это корректный красный gate, а не ошибка тестового раннера. Датированная квитанция не обещает неизменность будущего набора remote refs.

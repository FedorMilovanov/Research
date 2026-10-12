#!/usr/bin/env bash
# Добыча текстовых свидетелей под-корпуса ИСКУПЛЕНИЕ/nt.
#
# Зачем: tools/verify_nt_citations.py сверяет греческие цитаты карточек со
# свидетелем S1, но сам корпус в Git не хранится (00_NT_AUTHORITY §3: Git
# держит локаторы, не 9,8 МБ текста). Без этого скрипта проверка
# воспроизводится только на машине того, кто corpus уже скачал, — то есть
# не воспроизводится вовсе.
#
# Скрипт скачивает десять свидетелей по закреплённым SHA коммитов и сверяет
# sha256 набора текстовых файлов с пинами из 00_NT_AUTHORITY §3. Расхождение
# — это остановка с кодом 1, а не предупреждение: молча подменить текст
# свидетеля нельзя.
#
# Использование:
#   bash ИСКУПЛЕНИЕ/nt/tools/fetch_nt_corpus.sh
# Переменные:
#   NT_CORPUS_HOME  куда складывать (по умолчанию /home/user/nt-corpus)
#
# Скрипт ничего не пишет в репозиторий.

set -euo pipefail

HOME_DIR="${NT_CORPUS_HOME:-/home/user/nt-corpus}"

# id|owner/repo|sha|sha256 набора|подкаталог с текстом
WITNESSES=(
  "S1|morphgnt/py-sblgnt|904fed08a14bffea6e1776d8c4c3eeb7c6092688|f95833b147bb182786750700423625528dcb38f1508ea7585bce52e730a352f9|pysblgnt/sblgnt"
  "S2|byztxt/greektext-scrivener|6049a43b135ed870f843b83eb6a04764fc796678|61f4b97a80b2a8ec5faaf929f78a492b70e18fa7b4505e84983ee686782c19ea|textonly"
  "S3|byztxt/greektext-stephens|4314af2042d9e77b2ce5c1c86d0c49325dd81684|b94776ff4870570ee63240dfe36c9fc3f696600cfff39d408d85c4bb453ba4e9|textonly"
  "S4|byztxt/greektext-elzevir|94f31e2d2e8bd451d4d2f9739d13c419f7ce86c2|dbdc40702d84dcd889c2090c6be3b8ad6c49fa61efa3e3dbd69fd69b03768504|textonly"
  "S5|nathans/lxx-swete|26bad3eb42bba98471d154c954e36a6f30a0279d|5cf3ee82efa214caee9059ada09f67a1079fc397f3c1343aa1b72d8c49be5458|data"
  "S6|ETCBC/bhsa-min|f600a50fd902b6c9d31d67cf5611365df4169bce|51922d3bac47159d54a766748e6864449981f37939e31340b451fc67b1c62a4c|tf/2021"
  "S7|jjmccollum/sblgnt-tei|2a95589b2a9cb9b8bda5372650c7f55745ceecad|dc2888b956c63fe895fc5e809f1677e48455a6625c936a5bdb7e1fa2bd223462|xml"
  "S8|mrgreekgeek/tregelles-greek-nt|07ecf2165c9e404926365f5060b8150e0e19af49|52efbe59b499b9e366c8c90bfa6793c5b72a44f18011a8e8187fa7b1a29b7e32|verse-per-line"
  "S9|jjmccollum/comp-tc-mark|013b2f0db69cf577f866c75c82f5a98cbb558dc2|a9314ab4236e2d1a481e58cf7408542b014a28bfd7cf3439f414df5711d1159c|xml"
  "S10|jjmccollum/sbl-2023-talk|4ada2a729cc3e36ab29d101fe924e435d0a8bd54|5758c2bdcd837bcde92b7c1af250d23f50bf72f6769cd914b9788a9866c433a0|xml"
)

# ОПРЕДЕЛЕНИЕ sha256 набора (единое для всех четырёх свидетелей):
#   ( cd <каталог текста> && find . -type f | LC_ALL=C sort | xargs cat ) | sha256sum
# — конкатенация ВСЕХ файлов текстового каталога в лексикографическом порядке
# LC_ALL=C, без разделителей. Определение зафиксировано здесь и в
# 00_NT_AUTHORITY §3; любое другое определение даёт другой хеш.
#
# Пины S2–S4 выше ИСПРАВЛЕНЫ: ранее записанные значения
# 783e510d…/8f5bc4b8…/e7c730b9… не воспроизводились ни по одному из трёх
# опробованных определений набора и были невоспроизводимой записью. Новое
# определение выбрано не подгонкой: оно независимо воспроизводит пин S1
# f95833b1…, зафиксированный раньше и до появления этого скрипта.
set_sha256_of() {
  local dir="$1"
  ( cd "$dir" && find . -type f | LC_ALL=C sort | xargs cat ) | sha256sum | cut -d' ' -f1
}

mkdir -p "$HOME_DIR"
cd "$HOME_DIR"

fail=0
for entry in "${WITNESSES[@]}"; do
  IFS='|' read -r id repo sha want subdir <<<"$entry"
  name="${repo##*/}"
  dest="$HOME_DIR/${name}-${sha}"

  echo "--- $id  $repo @ ${sha:0:12}"

  if [ ! -d "$dest" ]; then
    echo "    скачиваю"
    curl -sSL --fail -o "${name}.tar.gz" \
      "https://codeload.github.com/${repo}/tar.gz/${sha}"
    tar xzf "${name}.tar.gz"
    rm -f "${name}.tar.gz"
  else
    echo "    уже есть"
  fi

  if [ ! -d "$dest/$subdir" ]; then
    echo "    ОШИБКА: нет каталога $dest/$subdir"
    fail=1
    continue
  fi

  got="$(set_sha256_of "$dest/$subdir")"
  nfiles="$( (cd "$dest/$subdir" && find . -type f | wc -l) | tr -d ' ')"
  if [ "$nfiles" -eq 0 ]; then
    # Защита от ложного «OK»: хеш пустого набора совпал бы сам с собой.
    echo "    ОШИБКА: каталог $subdir пуст, сверять нечего"
    fail=1
    continue
  fi
  if [ "$got" = "$want" ]; then
    echo "    sha256 OK  $got  ($nfiles файлов)"
  else
    echo "    sha256 РАСХОЖДЕНИЕ  ($nfiles файлов)"
    echo "      пин (00_NT_AUTHORITY §3): $want"
    echo "      получено:                 $got"
    fail=1
  fi
done

# S8 — Tregelles, The Greek New Testament (1857–1879), транскрипция Tyndale House
# Cambridge 2009 (D. Jongkind и др.). Права: текст XIX века — PD; цифровая
# транскрипция — CC BY-NC-SA 3.0. ВАЖНО: в транскрипции НЕТ аппарата, хотя
# титул издания обещает «with their Various Readings in Full» — проверено:
# 0 вхождений א и 0 сокращений версий (syr/arm/cop/vulg). Это текст, а не
# аппарат, поэтому рукописный уровень LOCATOR_HOLD он не закрывает. Ценность
# другая: это независимый критический текст, которым проверяется сам S7.

# S9 — колляция Марка ПО РУКОПИСЯМ: jjmccollum/comp-tc-mark, xml/ecm_mark.xml.
# TEI-колляция Марка во всех точках вариации UBS5, свидетели — все, которые
# покрывает Editio Critica Maior для Марка: 284 <witness>, включая Ausgangstext
# (сигла A), византийскую традицию (MT), папирусы P45 P84 P88 P137, унциалы
# 01 02 03 04 05 011 017 019 022 032 037 038 041-044 0211, минускулы, лекционарии
# (L…), версии (L:V лат. Vulg., S:V S:P S:H сир., Ä) и отцов (Chrys, Did, Epiph,
# Eus, Ir, Cyr, Phot, Or, AntEp). 148 юнитов в 119 стихах. Лицензия CC BY 4.0.
# ЗАЧЕМ: S7 атрибутирует чтения изданиям (#NA, #RP, #WH) и рукописей не даёт;
# S9 даёт именно рукописи. Это тот уровень, которого не хватало LOCATOR_HOLD.
#
# S10 — ещё пять колляций того же редактора: jjmccollum/sbl-2023-talk, xml/:
#   ecm_acts.xml        ECM Деяния — 9555 юнитов, 600 свидетелей, у каждого
#                       атрибут type= (papyrus 15, majuscule 33, minuscule 127,
#                       lectionary 13, version 56, father 124, corrector 232)
#   ecm_mark.xml        UBS Марк 2023 — 148 юнитов, 203 свидетеля (более ранняя
#                       и менее полная версия, чем S9; оставлена как перекрёстная
#                       проверка S9, а не как замена)
#   ubs_ephesians.xml   UBS Ефесянам — 42 юнита, 37 свидетелей
#   ubs_1_peter.xml     UBS 1 Петра  — 36 юнитов, 114 свидетелей
#   ubs_revelation.xml  UBS Откровение — 70 юнитов, 86 свидетелей
# Лицензия CC BY 4.0. ВНИМАНИЕ: нумерация книг в этих файлах НЕ стандартная —
# B26 здесь Откровение, а не Иуда (проверено по леммам юнитов и по числу глав:
# 22). tools/manuscript_collation.py определяет книгу сверкой с S1, а не по
# таблице, и печатает процент совпадений.
#
# S7 — критический аппарат SBLGNT (Holmes) в TEI: jjmccollum/sblgnt-tei.
# Лицензия CC BY 4.0 (сам SBLGNT перевыпущен под CC BY, репозиторий унаследовал
# лицензию) — это НЕ CC BY-NC и не CC BY-SA, как у S5/S6. 6929 записей <app>,
# 13 свидетелей. ГРАНИЦА: атрибуция идёт изданиям (NA27, WH, Treg, RP, NIV),
# а не рукописям — ни א, ни B, ни P46 здесь нет; TR цитируется всего 5 раз и
# только для целых добавленных стихов, поэтому для TR свидетелями остаются
# S2/S3/S4. Сужает LOCATOR_HOLD до рукописного уровня, но не снимает его.

# S6 — еврейский MT: ETCBC/bhsa-min, Text-Fabric 2021, датасет BHSA
# (Biblia Hebraica Stuttgartensia Amstelodamensis). Закрывает MT_HOLD: до S6
# утверждения вида «LXX передаёт כַּפֹּרֶת как ἱλαστήριον» были выводом из
# греческого соответствия. ПРАВA: LICENSE репозитория — MIT, но он покрывает
# только код дистилляции; данные по README репозитория BHSA идут под
# CC BY-NC 4.0 (DOI 10.17026/dans-z6y-skyh), коммерческое использование —
# только с согласия German Bible Society. Некоммерческое исследование и
# публикация результатов с атрибуцией разрешены. В Git не публикуется.

# S5 — LXX: Swete (ed.), The Old Testament in Greek, Cambridge 1901,
# в цифровой передаче First1KGreek через nathans/lxx-swete. Издание
# установлено по CTS-метаданным First1KGreek (tlg0527/tlg002/__cts__.xml),
# а не по имени репозитория. Права: текст — Swete 1901 (PD), цифровая
# передача — CC BY-SA 4.0; в Git не публикуется.

# Стабильный путь для проверяльщика: он по умолчанию смотрит в
# py-sblgnt-master, а tarball распаковывается в py-sblgnt-<sha>.
if [ -d "$HOME_DIR/py-sblgnt-904fed08a14bffea6e1776d8c4c3eeb7c6092688" ]; then
  ln -sfn "py-sblgnt-904fed08a14bffea6e1776d8c4c3eeb7c6092688" "$HOME_DIR/py-sblgnt-master"
fi

echo
if [ "$fail" -ne 0 ]; then
  echo "FAIL: хотя бы один свидетель не совпал с пином."
  exit 1
fi
echo "OK: все десять свидетелей скачаны и сверены с пинами."
echo "Корпус: $HOME_DIR"
echo "Дальше: python3 ИСКУПЛЕНИЕ/nt/tools/verify_nt_citations.py"

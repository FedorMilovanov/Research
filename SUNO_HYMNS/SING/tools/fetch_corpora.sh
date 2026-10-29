#!/usr/bin/env bash
# Докачка библейских корпусов для проверки серии SING.
# Всё скачивается в /tmp (песочница очищается между сессиями) — поэтому скрипт идемпотентен
# и его можно запускать заново. Архивы НЕ коммитятся в репозиторий: это исходники, а не данные.
#
#   ./fetch_corpora.sh            — всё
#   ./fetch_corpora.sh wlc        — только Ленинградский кодекс
set -euo pipefail

BIBLE=${BIBLE:-/tmp/bible}
CACHE=${CACHE:-/tmp/bible/_archives}
mkdir -p "$BIBLE" "$CACHE"

# want <раздел> [запрошенные разделы...] : если список пуст — разрешено всё
want() {
  local name=$1; shift
  [[ $# -eq 0 ]] && return 0
  local x; for x in "$@"; do [[ "$x" == "$name" ]] && return 0; done
  return 1
}

fetch() { # файл url
  [[ -s "$CACHE/$1" ]] && { echo "  $1 — уже скачан"; return; }
  echo "  $1 — скачиваю"
  curl -sL --retry 3 --retry-delay 2 -o "$CACHE/$1.part" "$2" && mv "$CACHE/$1.part" "$CACHE/$1"
}

# ---------- Новый Завет: morphgnt (текст с морфологией) ----------
if want sblgnt "$@"; then
  echo "== morphgnt/sblgnt =="
  fetch sblgnt.tgz https://codeload.github.com/morphgnt/sblgnt/tar.gz/refs/heads/master
  mkdir -p "$BIBLE/sblgnt"
  tar xzf "$CACHE/sblgnt.tgz" -C "$BIBLE/sblgnt" --strip-components=1
  echo "  файлов: $(ls "$BIBLE/sblgnt"/*-morphgnt.txt | wc -l)"
fi

# ---------- TR Скривенера 1894 (бета-код) ----------
if want tr "$@"; then
  echo "== byztxt/greektext-scrivener =="
  fetch tr.tgz https://codeload.github.com/byztxt/greektext-scrivener/tar.gz/refs/heads/master
  mkdir -p "$BIBLE/tr"
  tar xzf "$CACHE/tr.tgz" -C "$BIBLE/tr" --strip-components=1
  echo "  файлов: $(ls "$BIBLE/tr"/textonly/*.SCV 2>/dev/null | wc -l)"
fi

# ---------- Септуагинта Rahlfs 1935 (постихово, 28 861 стих) ----------
if want lxx "$@"; then
  echo "== eliranwong/LXX-Rahlfs-1935 (146 МБ, качается целиком, распаковка выборочная) =="
  fetch lxx.tgz https://codeload.github.com/eliranwong/LXX-Rahlfs-1935/tar.gz/refs/heads/master
  mkdir -p "$BIBLE/lxx"
  tar xzf "$CACHE/lxx.tgz" -C "$BIBLE/lxx" --strip-components=4 \
      "LXX-Rahlfs-1935-master/11_end-users_files/MyBible/Bibles/LXX_final_main.csv" \
      "LXX-Rahlfs-1935-master/11_end-users_files/MyBible/Bibles/books_main.csv"
  echo "  $(ls -la "$BIBLE/lxx" | tail -2)"
fi

# ---------- Синодальный перевод (USFM) ----------
if want rst "$@"; then
  echo "== onlydotbible/rst =="
  fetch rst.tgz https://codeload.github.com/onlydotbible/rst/tar.gz/refs/heads/master
  mkdir -p "$BIBLE/rst"
  tar xzf "$CACHE/rst.tgz" -C "$BIBLE/rst" --strip-components=3 --wildcards '*/usfm/rst66/*.usfm'
  echo "  файлов: $(ls "$BIBLE/rst"/*.usfm 2>/dev/null | wc -l)"
fi

# ---------- Ленинградский кодекс (еврейский текст с морфологией) ----------
# ВАЖНО: параллельная закачка теряет файлы — только последовательно и с проверкой числа.
if want wlc "$@"; then
  echo "== openscriptures/morphhb (40 книг, последовательно) =="
  mkdir -p "$BIBLE/wlc"
  mapfile -t names < <(gh api repos/openscriptures/morphhb/contents/wlc --jq '.[].name')
  for f in "${names[@]}"; do
    if [[ -s "$BIBLE/wlc/$f" ]]; then continue; fi
    for attempt in 1 2 3; do
      sha=$(gh api "repos/openscriptures/morphhb/contents/wlc/$f" --jq .sha) || continue
      gh api -H "Accept: application/vnd.github.raw" \
             "repos/openscriptures/morphhb/git/blobs/$sha" > "$BIBLE/wlc/$f.part" 2>/dev/null || continue
      [[ -s "$BIBLE/wlc/$f.part" ]] && mv "$BIBLE/wlc/$f.part" "$BIBLE/wlc/$f" && break
    done
  done
  n=$(ls "$BIBLE/wlc"/*.xml 2>/dev/null | wc -l)
  echo "  файлов: $n (должно быть 40)"
  [[ "$n" -eq 40 ]] || { echo "  ОШИБКА: недокачано"; exit 1; }
fi

echo "== готово: $BIBLE =="

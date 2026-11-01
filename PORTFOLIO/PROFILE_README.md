# Профиль GitHub и гигиена репозиториев

Документ для ручного применения: здесь нет автоматики, только готовые тексты и чек-листы. Всё проверено по состоянию на 1 ноября 2026.

---

## 1. Профиль-README

Создать **публичный** репозиторий с именем `FedorMilovanov` (совпадает с логином) и положить в него `README.md`. GitHub автоматически покажет файл на странице аккаунта.

### `README.md`

````markdown
# Фёдор Милованов · Fedor Milovanov

**Продуктовый инженер и технический редактор.** Строю продакшн-системы соло, управляя командой ИИ-агентов:
контракты → гейты → доказательная приёмка → живой продакшн.

**AI-native product builder.** I ship production systems solo by directing AI agents under
machine-checked contracts — and I make the result verifiable.

---

## Что работает прямо сейчас · Live

| Проект | Что это | Стек |
|---|---|---|
| [gospod-bog.ru](https://gospod-bog.ru) | Богословская библиотека: 111 страниц, десять атласов, офлайн-чтение, озвучка в браузере (интеграция открытого vosk-tts + свой слой ударений) | Astro · vanilla JS · ONNX |
| [thelegendarypoet.ru](https://thelegendarypoet.ru) | Редакционный сайт о русской поэзии и собственный API на Worker + D1 | React 19 · TS · Cloudflare |
| [milovicake.ru](https://milovicake.ru) | Коммерческий сайт кондитера: PWA, 14 гео-лендингов, ноль зависимостей | HTML/CSS/JS · Playwright |
| [french.milovicake.ru](https://french.milovicake.ru) | 157 статей о французской кондитерской школе | Astro SSG |
| [YouTube @fedormilovanov](https://www.youtube.com/@fedormilovanov) | Теологический архив: ≈1 781 публичный элемент за 11 лет; «Проповеди» — 699 видео, «Джон МакАртур» — 421, «Вопросы и ответы» — 199; дистрибуция в VK (≈2 879 видео) | YouTube API · VK API |
| [YouTube @TheLegendaryPoet](https://www.youtube.com/@TheLegendaryPoet) | Канал о русской поэзии: 153 видео, 1,32 тыс. подписчиков, музыка и клипы, собранные с ИИ | Suno · ИИ-визуал · монтаж |
| [@milovanovaibot](https://t.me/milovanovaibot) | Telegram-тренажёр по Первому посланию Петра и Mini App | Python · MongoDB |

## Цифры · Numbers

`5` живых продуктов · `241` CI-пайплайнов · `119 919` запусков CI · `1 390` тестовых и QA-файлов ·
`766 175` строк прикладного кода под управлением · `≈365 000` слов авторской прозы ·
`153` видео и `1,32 тыс.` подписчиков на канале о поэзии · `≈1 781` видео в теологическом архиве · `111` точных пар YouTube↔VK.

## Чем я занимаюсь · What I do

- **Agent orchestration and verification** — контракты, fail-closed гейты, посткондиции, `never_replay`, single-writer locks.
- **Editorial technology** — доказательные цифровые библиотеки: классы источников, локаторы, права, SEO, доступность.
- **AI media production** — музыка в Suno по своим текстам и промтам, ИИ-визуал и клипы, кросс-платформенная дистрибуция с точной идентичностью объектов.
- **Full-cycle product** — исследование → контент → сайт или бот → аналитика → эксплуатация.

## Как я работаю · How I work

1. Контракт до кода. 2. Fail closed. 3. Source ≠ build ≠ production. 4. Посткондиция вместо надежды.
5. Один владелец на поверхность. 6. Решённое уходит в архив. 7. Редакционная граница — за человеком.

## Контакты · Contact

[email] · [Telegram] · Санкт-Петербург, Россия (remote)
````

---

## 2. Описания репозиториев

Вставить в поле Description. Длина — до 160 символов, иначе GitHub обрежет в поиске.

| Репозиторий | Description | Topics |
|---|---|---|
| `gb-is-my-strength` | Theological research library: Astro site, interactive biblical atlases, offline reader, in-browser Russian TTS. Live: gospod-bog.ru | `astro` `static-site` `tts` `accessibility` `seo` `editorial` |
| `TheLegendaryPoet` | Editorial platform on Russian poetry — React 19 + TS, prerendered routes, Cloudflare Worker + D1 community API. Live: thelegendarypoet.ru | `react` `typescript` `vite` `cloudflare-workers` `d1` `editorial` |
| `Milovi_Cake` | Premium confectionery site: zero runtime dependencies, PWA, 14 geo landings, Playwright + Lighthouse gates. Live: milovicake.ru | `vanilla-js` `pwa` `playwright` `lighthouse-ci` `seo` `local-business` |
| `Milovi_School` | Astro SSG library: 157 sourced articles on the French pastry tradition, fail-closed SEO audits. Live: french.milovicake.ru | `astro` `static-site-generator` `json-ld` `seo` `content` |
| `mp3telegrambot` | Telegram pipeline: Gemini video analysis, Yandex LiveDub translation with semantic QA, MP3, summaries and Shorts | `python` `telegram-bot` `gemini` `ffmpeg` `asyncio` |
| `video-channel-manager` | Safety-first YouTube/VK/Instagram publishing: exact IDs, single-writer locks, postcondition reads, never_replay | `python` `sqlalchemy` `alembic` `youtube-api` `vk-api` `reliability` |
| `bible-bot` | Telegram bot and Mini App for studying 1 Peter: courses, PvP, leaderboards, MongoDB durable state | `python` `telegram-bot` `telegram-mini-app` `mongodb` `education` |
| `Research` | Evidence-based research backend: source classes A1–D, HOLD flags, machine-checked authority registries | `research` `knowledge-base` `python` `evidence` `governance` |
| `AuditRepo` | Multi-agent audit system: evidence, verification, root-cause, compact MASTER, retirement | `audit` `ai-agents` `verification` `process` |
| `DeepMovieReview` | Evidence-backed film analysis: Next.js App Router, scene-verified edition state machine, structured spoiler data | `nextjs` `typescript` `film` `editorial` `content-modeling` |
| `gb-vosk-tts` | Browser integration of the open-source vosk-tts engine (Apache-2.0) plus a Russian stress layer; differential tests against the Python package | `tts` `vosk` `onnxruntime` `russian` `accessibility` |

## 3. Лицензии

- **MIT** — инструменты и библиотеки: `mp3telegrambot`, `video-channel-manager`, `gb-vosk-tts`, `AuditRepo`.
- **Проприетарно, с явной оговоркой о контенте** — контентные проекты: `gb-is-my-strength`, `TheLegendaryPoet`, `Milovi_Cake`, `Milovi_School`, `Research`, `DeepMovieReview`.

Формулировка для контентных проектов (файл `LICENSE` или раздел в README): «Код доступен для ознакомления. Тексты, переводы, изображения и аудиоматериалы — all rights reserved; копирование и перепубликация без письменного разрешения не допускаются». Без этого условия любой может легально перепубликовать библиотеку целиком.

---

## 4. Что закрепить

Порядок важен: первые три позиции читают почти всегда.

1. `gb-is-my-strength` — флагман, максимальный объём, живой домен.
2. `video-channel-manager` — самый зрелый инженерный артефакт для технической аудитории.
3. `mp3telegrambot` — 208 тысяч строк, ИИ-пайплайн, продакшн-дисциплина.
4. `TheLegendaryPoet` — современный стек и собственный backend.
5. `Milovi_Cake` — коммерческое доказательство: сайт приносит заказы.
6. `AuditRepo` — метод, то есть главный дифференциатор.

`DeepMovieReview` и `gb-vosk-tts` — во вторую линию, после появления английских README. `gb-vosk-tts` не выставлять вперёд до решения по лицензии (см. `AUDIT_RU.md` R11): движок чужой, а заявленный MIT поверх производного от Apache-2.0 требует проверки.

---

## 5. Что убрать с витрины

| Репозиторий | Действие | Причина |
|---|---|---|
| `baptist---2` | Архивировать или удалить | пустой, 0 байт |
| `baptist2` | Архивировать | заглушка из двух файлов |
| `baptist` | Архивировать | брошенный прототип, шесть коммитов |
| `FedorMilovanov.github.io` | Оставить, добавить описание «redirect hub» | 155 МБ медиа при одном редиректе — сжать или вынести медиа |

Правило простое: на профиле не должно быть ничего, что читается как «не довёл».

---

## 6. Настройки профиля

- [ ] **Bio** (до 160 символов): `Строю продукты с ИИ-агентами и делаю их проверяемыми: контракты, CI-гейты, доказательная приёмка. Пять живых проектов.`
- [ ] **Location:** Санкт-Петербург, Россия.
- [ ] **Website:** ссылка на портфолио; до его появления — `gospod-bog.ru`.
- [ ] **Social links:** Telegram, LinkedIn, почта.
- [ ] **Двухфакторная аутентификация** и Dependabot alerts на всех репозиториях: для зарубежного заказчика это маркер профессионализма, для тебя — защита активов.

---

## 7. Файл, который стоит добавить в каждый крупный репозиторий

`CASE_STUDY.md` в корне — сокращённая версия кейса из `PORTFOLIO_RU.md`: задача → что сделано → механизм → доказательства → метрики.

Причина простая: рекрутер не читает шестьдесят тысяч строк и не открывает `docs/`. Он смотрит README первые пятнадцать секунд и один файл с результатом. Сейчас README большинства проектов написаны для агентов — «authority», «lane», «fail-closed», — а не для человека, который решает, звать ли тебя на работу.

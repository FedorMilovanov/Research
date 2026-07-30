# Official digital collections — HTTP link audit

**Дата проверки:** 30 июля 2026 года  
**Источник:** `SOURCE_LIBRARY/OFFICIAL_DIGITAL_COLLECTIONS_70PLUS_INDEX_2026-07-30.md`  
**Workflow run:** `30504169418`  
**Job:** `90750193358`

## Итог

Проверены все **94 уникальных URL** из официального индекса:

- `OK`: 81;
- `REACHABLE_RESTRICTED` (HTTP 403): 8;
- `TIMEOUT`: 4;
- `NETWORK_ERROR`: 1;
- `DEAD` (404/410): **0**;
- severe DNS/TLS errors: 0.

Вывод: в индексе не обнаружено подтверждённых мёртвых ссылок. Ограничения относятся преимущественно к автоматизированному runner-доступу и не означают, что официальная коллекция исчезла.

## Reachable but restricted

Следующие официальные адреса вернули HTTP 403 GitHub-hosted runner:

1. Library of Congress, item `05012205`;
2. Library of Congress, Waliszewski resource;
3. Library of Congress, eighteenth-century Russian publications resource;
4. Library of Congress, Russian-language books search;
5. Cambridge Digital Library;
6. BnF Archives et manuscrits;
7. HathiTrust;
8. WorldCat Search.

Статус: `REACHABLE_RESTRICTED`, а не `DEAD`. Эти сайты могут требовать браузерные cookies, JavaScript, региональную маршрутизацию или блокировать automation user agents.

## Timeouts

GitHub runner не получил ответ в установленное время от:

- Digital Bodleian;
- Государственного каталога Музейного фонда РФ;
- исторической электронной библиотеки ИМЛИ РАН;
- текущего издательского портала ИМЛИ РАН.

Это согласуется с предыдущим ИМЛИ access-audit: серверы могут быть доступны обычному браузеру, но недоступны из Azure/GitHub runner. Ссылки сохраняются с пометкой `MANUAL-BROWSER-CHECK / RUNNER-TIMEOUT`.

## Network error

`https://pushkin-digital.ru/` вернул runner-ошибку `Network is unreachable`.

Решение:

- не объявлять адрес мёртвым по одному Azure-runner результату;
- проверить вручную из пользовательской браузерной среды;
- до подтверждения пометить `MANUAL-BROWSER-CHECK`;
- не использовать как единственный источник production-утверждения.

## Стабильные редиректы

13 ссылок успешно перенаправлены на рабочие конечные URL. В частности, старые NYPL UUID перенаправляются на новые item UUID с `canvasIndex=0`.

Это полезный признак обратной совместимости NYPL. Исходные ссылки пока можно сохранять, но при следующей редакции индекса целесообразно нормализовать их до текущих canonical URL.

Также наблюдались рабочие редиректы:

- Europeana → `/en`;
- Gallica → французская landing page;
- BnF catalogue → `index.do`;
- Bakhrushin Museum → `www` host.

## Граница интерпретации

HTTP `200/206` означает только техническую доступность endpoint. Он не подтверждает:

- правильность подписи объекта;
- авторство;
- дату;
- лицензию;
- право повторной публикации;
- пригодность для конкретного утверждения или визуала.

Для production по-прежнему необходим item-level rights/provenance review.

## Воспроизводимые файлы

Workflow artifact `official-digital-collections-link-audit` содержит:

- `official-collections-link-audit.json`;
- `official-collections-link-audit.csv`;
- `OFFICIAL_COLLECTIONS_LINK_AUDIT.md`.

Скрипт:

```text
SOURCE_LIBRARY/tools/audit_official_collection_links.py
```

Workflow:

```text
.github/workflows/audit-official-digital-collections-links.yml
```

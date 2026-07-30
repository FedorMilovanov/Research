# Портретные референсы поэтов: category-first review workflow

**Дата:** 30 июля 2026 года  
**Статус:** `CANDIDATE DISCOVERY / CONTACT SHEETS / HUMAN IDENTITY REVIEW / ORIGINAL DOWNLOAD LATER`

## Почему изменён подход

Полнотекстовый поиск Wikimedia Commons по имени человека регулярно возвращает объекты, названные в его честь:

- теплоходы;
- музеи и дома;
- памятники и могилы;
- мемориальные таблички;
- книги и конверты;
- литературные премии;
- современные исполнители, играющие роль поэта.

Формальная открытая лицензия и наличие имени в заголовке не делают такой файл портретом. Поэтому итоговый reference ZIP нельзя формировать одним поисковым запросом.

## Новый процесс

1. Начать с точной Commons-категории конкретного человека.
2. Получить только файлы из пространства `File`.
3. Дополнить title-search лишь когда в категории недостаточно кандидатов.
4. Проверить структурированную лицензию.
5. Исключить явные non-person object markers по title, description и categories.
6. Скачать только review-thumbnail шириной 512 px.
7. Построить контактные листы по 4 изображения в строке.
8. Визуально подтвердить личность и тип изображения.
9. Составить отдельный allowlist финальных карточек.
10. Только после этого скачать неизменённые оригиналы и сохранить SHA-256/credit line.

## Люди

- Сергей Есенин;
- Иван Бунин;
- Игорь Северянин;
- Константин Бальмонт;
- Фёдор Тютчев;
- Аполлон Майков;
- Валерий Брюсов;
- Александр Блок;
- Афанасий Фет;
- Владимир Маяковский;
- Анна Ахматова;
- Николай Гумилёв;
- Борис Пастернак;
- Александр Пушкин;
- Михаил Лермонтов;
- Марина Цветаева;
- Осип Мандельштам;
- Велимир Хлебников;
- Зинаида Гиппиус.

## Лицензионный gate

Принимаются только:

- Public Domain;
- CC0;
- CC BY;
- CC BY-SA.

Исключаются:

- Fair use;
- copyrighted;
- all rights reserved;
- NonCommercial;
- NoDerivatives.

Review-thumbnail не является production-asset. Итоговая атрибуция строится по карточке оригинала, а не по превью.

## Автоматические object-type исключения

Фильтр анализирует title, image description и categories. Исключаются признаки:

```text
museum, house, grave, tomb, plaque, monument, statue, bust,
estate, street, school, library, book, cover, autograph,
signature, memorial, stamp, coin, quote, family, group,
river, reservoir, port, ship, cruise, boat, letter,
manuscript, literary prize, concert hall, envelope, garden,
villa, apartment, exhibition, poster, graffiti, performance,
information, wall
```

и русские эквиваленты.

Автоматический фильтр снижает шум, но не заменяет визуальную идентификацию.

## Пакет review

```text
portrait-review-output/
├── thumbnails/
│   ├── Sergei_Yesenin__01.jpg
│   └── ...
├── contact-sheets/
│   ├── portrait-review-sheet-01.jpg
│   └── ...
├── portrait-candidates.json
├── portrait-candidates.csv
└── README.md
```

Manifest сохраняет:

- имя человека;
- Commons category;
- File title;
- description page;
- original URL;
- thumbnail URL;
- MIME и размеры;
- лицензию и attribution requirement;
- автора, credit, source и дату;
- description/categories;
- статус автоматического отбора;
- SHA-256 review-thumbnail.

## Ручной gate

Финальный кандидат получает `APPROVED_REFERENCE` только когда:

1. на изображении действительно нужный человек;
2. подпись Commons согласуется с иконографией;
3. изображение пригодно для распознавания лица;
4. это не памятник, актёр, родственник или объект имени поэта;
5. дата/возраст не противоречат задаче;
6. нет смыслового дубля уже выбранного изображения;
7. известна карточка оригинала;
8. права и credit line понятны.

Для девяти исходных проблемных поэтов цель — по пять подтверждённых изображений каждого. Для остальных авторов набор расширяет будущий «зал поэтов».

## Хранение

- Contact sheets и thumbnails: Research artifact / private archive.
- Финальные оригиналы: частный Drive/Library после approve.
- GitHub: код, manifest без тяжёлых бинарников, allowlist и rights decisions.
- Production: только отдельно разрешённые assets.

## Запуск

```bash
python SOURCE_LIBRARY/tools/build_poet_portrait_review_candidates.py \
  --category-limit 150 \
  --search-limit 50 \
  --per-person 8 \
  --minimum-ready 70 \
  --output portrait-review-output
```

Workflow:

```text
.github/workflows/build-poet-portrait-review-candidates.yml
```

# classrooms

ЛР3 — каталог учебных аудиторий.

## Запуск

```
pip install -e ".[dev]"
pytest
python main.py
```

`main.py` создаёт небольшой каталог, ищет в нём, сохраняет в `catalog.json` и загружает обратно.

## Аудитория

`Classroom` — dataclass с полями `id`, `name`, `category`, `year`, `building` (корпус),
`capacity` (вместимость).

Проверки при создании (иначе `InvalidItemError`):
- `id`, `name`, `category`, `building` — непустые строки;
- `year` — целое число от 1800 до 2026;
- `capacity` — целое число больше 0.

Класс `frozen`, поэтому после создания поля менять нельзя.

## Каталог

`Catalog` хранит аудитории в словаре `{id: аудитория}`.

- `add(item)` — добавить; повтор id → `DuplicateIdError`
- `get(item_id)` — получить; нет id → `ItemNotFoundError`
- `remove(item_id)` — удалить; нет id → `ItemNotFoundError`
- `find_by_category(category)` — поиск по категории без учёта регистра
- `find_by_name(query)` — поиск по части названия без учёта регистра
- `len(catalog)`, `id in catalog`, `for room in catalog`

`get` работает за O(1), потому что берёт значение из словаря по ключу.
`find_by_name` работает за O(n), потому что проверяет каждую аудиторию.

Поиск всегда возвращает новый список, поэтому изменение результата не меняет каталог.

Порядок обхода — порядок добавления.

## JSON

```json
{
  "format_version": 1,
  "items": [
    {"id": "A-101", "name": "Лекционная 101", "category": "лекционная",
     "year": 2015, "building": "А", "capacity": 120}
  ]
}
```

`save_catalog(catalog, path)` и `load_catalog(catalog, path)`.

При загрузке все аудитории сначала читаются в новый каталог, и только если ошибок не было,
старый каталог заменяется. Поэтому битый файл ничего не портит.

- версия не 1 → `UnsupportedVersionError`
- любая другая проблема с файлом → `CorruptedFileError`

## Ошибки

Все ошибки наследуются от `CatalogError`: `InvalidItemError`, `DuplicateIdError`,
`ItemNotFoundError`, `UnsupportedVersionError`, `CorruptedFileError`.

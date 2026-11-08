"""Каталог учебных аудиторий."""

from collections.abc import Iterator

from classrooms.errors import DuplicateIdError, InvalidItemError, ItemNotFoundError
from classrooms.model import Classroom


class Catalog:
    """Каталог аудиторий {id: аудитория}"""

    def __init__(self) -> None:
        self._items: dict[str, Classroom] = {}

    def add(self, item: Classroom) -> None:
        if not isinstance(item, Classroom):
            raise InvalidItemError("в каталог можно добавить только Classroom")
        if item.id in self._items:
            raise DuplicateIdError(f"id {item.id} уже есть в каталоге")
        self._items[item.id] = item

    def get(self, item_id: str) -> Classroom:
        if item_id not in self._items:
            raise ItemNotFoundError(f"id {item_id} не найден")
        return self._items[item_id]

    def remove(self, item_id: str) -> None:
        if item_id not in self._items:
            raise ItemNotFoundError(f"id {item_id} не найден")
        del self._items[item_id]

    def find_by_category(self, category: str) -> list[Classroom]:
        result = []
        for item in self._items.values():
            if item.category.lower() == category.lower():
                result.append(item)
        return result

    def find_by_name(self, query: str) -> list[Classroom]:
        result = []
        for item in self._items.values():
            if query.lower() in item.name.lower():
                result.append(item)
        return result

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Classroom]:
        return iter(self._items.values())

    def __contains__(self, item_id: object) -> bool:
        return item_id in self._items

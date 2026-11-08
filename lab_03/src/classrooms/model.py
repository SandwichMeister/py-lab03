"""Учебная аудитория"""

from dataclasses import dataclass

from classrooms.errors import InvalidItemError


def is_empty_text(value: object) -> bool:
    return not isinstance(value, str) or value.count(" ") == len(value)


@dataclass(frozen=True)
class Classroom:
    """Учебная аудитория"""

    id: str  # "A-301"
    name: str  # "Лекционная аудитория 301"
    category: str  # "лекционная", "лаборатория" ...
    year: int  # год ввода в эксплуатацию
    building: str  # корпус
    capacity: int  # вместимость

    def __post_init__(self) -> None:

        if is_empty_text(self.id):
            raise InvalidItemError("id должен быть непустой строкой")
        if is_empty_text(self.name):
            raise InvalidItemError("name должен быть непустой строкой")
        if is_empty_text(self.category):
            raise InvalidItemError("category должен быть непустой строкой")
        if is_empty_text(self.building):
            raise InvalidItemError("building должен быть непустой строкой")
        if not isinstance(self.year, int) or self.year < 1800 or self.year > 2026:
            raise InvalidItemError("year должен быть целым числом от 1800 до 2026")
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise InvalidItemError("capacity должен быть целым числом больше 0")

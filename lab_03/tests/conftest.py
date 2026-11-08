import pytest

from classrooms import Catalog, Classroom


def make_room(**changes) -> Classroom:
    data = {
        "id": "A-101",
        "name": "Лекционная аудитория 101",
        "category": "лекционная",
        "year": 2015,
        "building": "А",
        "capacity": 120,
    }
    data.update(changes)
    return Classroom(**data)


@pytest.fixture
def catalog() -> Catalog:
    c = Catalog()
    c.add(make_room(id="A-101", name="Лекционная аудитория 101", category="лекционная"))
    c.add(make_room(id="B-205", name="Компьютерный класс 205", category="компьютерный класс"))
    c.add(make_room(id="A-102", name="ЛЕКЦИОННАЯ аудитория 102", category="лекционная"))
    return c

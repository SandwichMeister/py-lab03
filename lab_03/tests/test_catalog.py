import pytest

from classrooms import Catalog, DuplicateIdError, InvalidItemError, ItemNotFoundError
from conftest import make_room


def test_add_get_remove():
    c = Catalog()
    room = make_room()
    c.add(room)
    assert c.get("A-101") == room
    c.remove("A-101")
    assert "A-101" not in c


def test_errors(catalog):
    with pytest.raises(DuplicateIdError):
        catalog.add(make_room(id="A-101"))
    with pytest.raises(ItemNotFoundError):
        catalog.get("Z-999")
    with pytest.raises(ItemNotFoundError):
        catalog.remove("Z-999")
    with pytest.raises(InvalidItemError):
        catalog.add("не аудитория")
    assert len(catalog) == 3


def test_find_by_category(catalog):
    assert [r.id for r in catalog.find_by_category("лекционная")] == ["A-101", "A-102"]
    assert [r.id for r in catalog.find_by_category("ЛЕКЦИОННАЯ")] == ["A-101", "A-102"]
    assert catalog.find_by_category("булочная") == []


def test_find_by_name(catalog):
    assert [r.id for r in catalog.find_by_name("лекц")] == ["A-101", "A-102"]
    assert [r.id for r in catalog.find_by_name("ЛеКц")] == ["A-101", "A-102"]
    assert catalog.find_by_name("бассейн") == []


def test_search_result_is_copy(catalog):
    catalog.find_by_category("лекционная").clear()
    assert len(catalog.find_by_category("лекционная")) == 2


def test_len_in_iter(catalog):
    assert len(catalog) == 3
    assert "B-205" in catalog
    assert "Z-999" not in catalog
    assert [r.id for r in catalog] == ["A-101", "B-205", "A-102"]
    assert [r.id for r in catalog] == ["A-101", "B-205", "A-102"]

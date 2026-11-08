import pytest

from classrooms import InvalidItemError
from conftest import make_room


def test_valid_room():
    room = make_room()
    assert room.id == "A-101"
    assert room.year == 2015
    assert room.capacity == 120


@pytest.mark.parametrize("bad", [
    {"id": ""},
    {"id": "   "},
    {"name": ""},
    {"name": 123},
    {"category": " "},
    {"building": ""},
    {"year": 1500},
    {"year": 3000},
    {"year": "2015"},
    {"capacity": 0},
    {"capacity": -5},
    {"capacity": "120"},
    {"capacity": 12.5},
])
def test_invalid_room(bad):
    with pytest.raises(InvalidItemError):
        make_room(**bad)


def test_room_cannot_be_changed():
    room = make_room()
    with pytest.raises(AttributeError):
        room.capacity = -1

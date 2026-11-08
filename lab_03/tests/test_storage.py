import json

import pytest

from classrooms import (
    Catalog,
    CorruptedFileError,
    UnsupportedVersionError,
    load_catalog,
    save_catalog,
)

ROOM = {"id": "C-1", "name": "Ауд. C-1", "category": "лекционная",
        "year": 2020, "building": "В", "capacity": 50}


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)


def test_save_and_load(catalog, tmp_path):
    path = tmp_path / "catalog.json"
    save_catalog(catalog, path)

    with open(path, encoding="utf-8") as file:
        assert json.load(file)["format_version"] == 1

    loaded = Catalog()
    load_catalog(loaded, path)
    assert list(loaded) == list(catalog)


def test_unknown_version(catalog, tmp_path):
    path = tmp_path / "v2.json"
    write_json(path, {"format_version": 2, "items": [ROOM]})
    with pytest.raises(UnsupportedVersionError):
        load_catalog(catalog, path)
    assert len(catalog) == 3


def test_not_json(catalog, tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"format_version": 1, "items": [', encoding="utf-8")
    with pytest.raises(CorruptedFileError):
        load_catalog(catalog, path)
    assert len(catalog) == 3


@pytest.mark.parametrize("data", [
    {"format_version": 1},
    {"items": [ROOM]},
    {"format_version": 1, "items": [{"id": "C-1"}]},
    {"format_version": 1, "items": [ROOM, ROOM]},
    {"format_version": 1, "items": [ROOM, dict(ROOM, id="C-2", capacity=-1)]},
])
def test_broken_file_does_not_change_catalog(catalog, tmp_path, data):
    before = list(catalog)
    path = tmp_path / "bad.json"
    write_json(path, data)
    with pytest.raises(CorruptedFileError):
        load_catalog(catalog, path)
    assert list(catalog) == before

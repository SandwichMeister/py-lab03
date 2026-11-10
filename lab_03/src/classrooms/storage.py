"""Сохранение и загрузка каталога в JSON."""

import json
from dataclasses import asdict

from classrooms.catalog import Catalog
from classrooms.errors import (
    CorruptedFileError,
    DuplicateIdError,
    InvalidItemError,
    UnsupportedVersionError,
)
from classrooms.model import Classroom

FORMAT_VERSION = 1


def save_catalog(catalog: Catalog, path: str) -> None:
    data = {
        "format_version": FORMAT_VERSION,
        "items": [asdict(item) for item in catalog],
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_catalog(catalog: Catalog, path: str) -> None:
    """Загружает каталог из файла"""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise CorruptedFileError("корень JSON должен быть словарем")

        if set(data) != {"format_version", "items"}:
            raise CorruptedFileError("документ должен содержать только format_version и items")

        version = data["format_version"]

        if version != FORMAT_VERSION:
            raise UnsupportedVersionError(f"неизвестная версия формата: {version}")

        if not isinstance(data["items"], list):
            raise CorruptedFileError("items должен быть списком")

        required_fields = {"id", "name", "category", "year", "building", "capacity"}
        new_catalog = Catalog()

        for item_data in data["items"]:
            if set(item_data) != required_fields:
                raise CorruptedFileError("неверный набор полей аудитории")

            new_catalog.add(Classroom(**item_data))

    except (ValueError, TypeError, InvalidItemError, DuplicateIdError) as error:
        raise CorruptedFileError(f"файл повреждён: {error}") from error
    catalog._items = new_catalog._items  # ошибок не было — подменяем содержимое
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
        version = data["format_version"]
        items = data["items"]
    except (ValueError, KeyError, TypeError) as error:
        raise CorruptedFileError(f"файл повреждён: {error}") from error

    if version != FORMAT_VERSION:
        raise UnsupportedVersionError(f"неизвестная версия формата: {version}")

    new_catalog = Catalog()
    try:
        for item_data in items:
            new_catalog.add(Classroom(**item_data))
    except (TypeError, InvalidItemError, DuplicateIdError) as error:
        raise CorruptedFileError(f"файл повреждён: {error}") from error

    catalog._items = new_catalog._items  # ошибок не было — подменяем содержимое

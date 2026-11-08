"""Иерархия исключений каталога аудиторий."""


class CatalogError(Exception):
    """Базовая ошибка каталога. Все остальные ошибки пакета наследуются от неё."""


class InvalidItemError(CatalogError):
    """Сущность нарушает инвариант (пустой ID, неверная вместимость и т.п.)."""


class DuplicateIdError(CatalogError):
    """В каталоге уже есть объект с таким ID."""


class ItemNotFoundError(CatalogError):
    """Объект с указанным ID отсутствует в каталоге."""


class UnsupportedVersionError(CatalogError):
    """Документ JSON имеет неизвестное значение format_version."""


class CorruptedFileError(CatalogError):
    """Документ JSON повреждён: невалидный JSON, нет полей, неверные типы."""

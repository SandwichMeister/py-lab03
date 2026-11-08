from classrooms import Catalog, CatalogError, Classroom, load_catalog, save_catalog


def main() -> None:
    catalog = Catalog()
    catalog.add(Classroom("A-101", "Лекционная аудитория 101", "лекционная", 2015, "А", 120))
    catalog.add(Classroom("B-205", "Компьютерный класс 205", "компьютерный класс", 2020, "Б", 24))
    catalog.add(Classroom("A-310", "Лаборатория физики", "лаборатория", 2018, "А", 30))

    print("Все аудитории:")
    for room in catalog:
        print(" ", room.id, room.name, room.capacity)

    print("Поиск 'класс':", [room.id for room in catalog.find_by_name("класс")])
    print("Лекционные:", [room.id for room in catalog.find_by_category("лекционная")])

    try:
        catalog.add(Classroom("A-101", "Дубликат", "лекционная", 2015, "А", 10))
    except CatalogError as error:
        print("Ошибка:", error)

    save_catalog(catalog, "catalog.json")
    loaded = Catalog()
    load_catalog(loaded, "catalog.json")
    print("Сохранено и загружено обратно:", len(loaded), "аудитории")


if __name__ == "__main__":
    main()

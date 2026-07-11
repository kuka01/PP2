import csv
import json
from datetime import datetime

import psycopg2
from connect import connect


def print_rows(rows):
    if not rows:
        print("Ничего не найдено.")
        return

    for row in rows:
        print(row)


def show_all(cursor):
    cursor.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name AS group_name,
            c.phone,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.id
        """
    )

    print("\n===== ВСЕ КОНТАКТЫ =====")
    print_rows(cursor.fetchall())


def search_all(cursor):
    query = input("Введите имя, email или телефон: ").strip()

    cursor.execute(
        "SELECT * FROM search_contacts(%s);",
        (query,)
    )

    print("\n===== РЕЗУЛЬТАТ ПОИСКА =====")
    print_rows(cursor.fetchall())


def filter_by_group(cursor):
    cursor.execute("SELECT name FROM groups ORDER BY name;")
    groups = cursor.fetchall()

    print("\nДоступные группы:")
    for group in groups:
        print("-", group[0])

    group_name = input("Введите название группы: ").strip()

    cursor.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            c.phone,
            c.created_at
        FROM contacts c
        JOIN groups g ON g.id = c.group_id
        WHERE g.name ILIKE %s
        ORDER BY c.name
        """,
        (group_name,)
    )

    print("\n===== КОНТАКТЫ ГРУППЫ =====")
    print_rows(cursor.fetchall())


def search_by_email(cursor):
    email_part = input("Введите часть email, например gmail: ").strip()

    cursor.execute(
        """
        SELECT id, name, email, birthday
        FROM contacts
        WHERE email ILIKE %s
        ORDER BY name
        """,
        (f"%{email_part}%",)
    )

    print("\n===== ПОИСК ПО EMAIL =====")
    print_rows(cursor.fetchall())


def sort_contacts(cursor):
    print("\n1. По имени")
    print("2. По дню рождения")
    print("3. По дате добавления")

    choice = input("Выберите сортировку: ").strip()

    allowed_orders = {
        "1": "c.name ASC",
        "2": "c.birthday ASC NULLS LAST",
        "3": "c.created_at DESC",
    }

    order_by = allowed_orders.get(choice)

    if order_by is None:
        print("Неверный выбор.")
        return

    query = f"""
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            g.name,
            c.created_at
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY {order_by}
    """

    cursor.execute(query)

    print("\n===== ОТСОРТИРОВАННЫЕ КОНТАКТЫ =====")
    print_rows(cursor.fetchall())


def pagination(cursor):
    try:
        page_size = int(input("Сколько контактов на странице? "))
        if page_size <= 0:
            print("Размер страницы должен быть больше нуля.")
            return
    except ValueError:
        print("Нужно ввести число.")
        return

    page = 0

    while True:
        offset = page * page_size

        cursor.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s);",
            (page_size, offset)
        )

        rows = cursor.fetchall()

        print(f"\n===== СТРАНИЦА {page + 1} =====")

        if rows:
            print_rows(rows)
        else:
            print("На этой странице нет контактов.")

        command = input(
            "\n[n] next, [p] previous, [q] quit: "
        ).strip().lower()

        if command == "n":
            if rows:
                page += 1
            else:
                print("Следующей страницы нет.")

        elif command == "p":
            if page > 0:
                page -= 1
            else:
                print("Это первая страница.")

        elif command == "q":
            break

        else:
            print("Неизвестная команда.")


def add_phone(cursor, conn):
    name = input("Имя существующего контакта: ").strip()
    phone = input("Новый телефон: ").strip()
    phone_type = input("Тип home/work/mobile: ").strip().lower()

    try:
        cursor.execute(
            "CALL add_phone(%s, %s, %s);",
            (name, phone, phone_type)
        )
        conn.commit()
        print("Телефон успешно добавлен.")

    except psycopg2.Error as error:
        conn.rollback()
        print("Ошибка:", error)


def move_to_group(cursor, conn):
    name = input("Имя контакта: ").strip()
    group_name = input("Новая группа: ").strip()

    try:
        cursor.execute(
            "CALL move_to_group(%s, %s);",
            (name, group_name)
        )
        conn.commit()
        print("Контакт перемещён в группу.")

    except psycopg2.Error as error:
        conn.rollback()
        print("Ошибка:", error)


def export_to_json(cursor):
    cursor.execute(
        """
        SELECT
            c.id,
            c.name,
            c.email,
            c.birthday,
            c.created_at,
            g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.id
        """
    )

    contacts = []

    for contact_row in cursor.fetchall():
        contact_id = contact_row[0]

        cursor.execute(
            """
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s
            ORDER BY id
            """,
            (contact_id,)
        )

        phones = [
            {
                "phone": phone_row[0],
                "type": phone_row[1]
            }
            for phone_row in cursor.fetchall()
        ]

        contacts.append(
            {
                "id": contact_row[0],
                "name": contact_row[1],
                "email": contact_row[2],
                "birthday": (
                    contact_row[3].isoformat()
                    if contact_row[3]
                    else None
                ),
                "created_at": (
                    contact_row[4].isoformat()
                    if contact_row[4]
                    else None
                ),
                "group": contact_row[5],
                "phones": phones,
            }
        )

    filename = input(
        "Имя JSON-файла [contacts.json]: "
    ).strip() or "contacts.json"

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            contacts,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(f"Экспорт завершён: {filename}")


def get_or_create_group(cursor, group_name):
    if not group_name:
        return None

    cursor.execute(
        """
        INSERT INTO groups(name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        """,
        (group_name,)
    )

    cursor.execute(
        "SELECT id FROM groups WHERE name = %s;",
        (group_name,)
    )

    result = cursor.fetchone()
    return result[0] if result else None


def import_from_json(cursor, conn):
    filename = input(
        "Имя JSON-файла [contacts.json]: "
    ).strip() or "contacts.json"

    try:
        with open(filename, "r", encoding="utf-8") as file:
            contacts = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError) as error:
        print("Ошибка чтения JSON:", error)
        return

    for item in contacts:
        name = str(item.get("name", "")).strip()

        if not name:
            print("Пропущен контакт без имени.")
            continue

        cursor.execute(
            """
            SELECT id
            FROM contacts
            WHERE name = %s
            ORDER BY id
            LIMIT 1
            """,
            (name,)
        )

        duplicate = cursor.fetchone()

        if duplicate:
            answer = input(
                f'Контакт "{name}" уже существует. '
                "[s] skip / [o] overwrite: "
            ).strip().lower()

            if answer != "o":
                print("Пропущен:", name)
                continue

            contact_id = duplicate[0]
            group_id = get_or_create_group(
                cursor,
                item.get("group")
            )

            cursor.execute(
                """
                UPDATE contacts
                SET email = %s,
                    birthday = %s,
                    group_id = %s
                WHERE id = %s
                """,
                (
                    item.get("email"),
                    item.get("birthday"),
                    group_id,
                    contact_id,
                )
            )

            cursor.execute(
                "DELETE FROM phones WHERE contact_id = %s;",
                (contact_id,)
            )

        else:
            group_id = get_or_create_group(
                cursor,
                item.get("group")
            )

            cursor.execute(
                """
                INSERT INTO contacts(
                    name,
                    email,
                    birthday,
                    group_id
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    name,
                    item.get("email"),
                    item.get("birthday"),
                    group_id,
                )
            )

            contact_id = cursor.fetchone()[0]

        for phone_data in item.get("phones", []):
            phone = str(phone_data.get("phone", "")).strip()
            phone_type = str(
                phone_data.get("type", "mobile")
            ).strip().lower()

            if not phone:
                continue

            if phone_type not in ("home", "work", "mobile"):
                phone_type = "mobile"

            cursor.execute(
                """
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
                ON CONFLICT (contact_id, phone) DO NOTHING
                """,
                (contact_id, phone, phone_type)
            )

    conn.commit()
    print("Импорт JSON завершён.")


def import_from_csv(cursor, conn):
    filename = input(
        "Имя CSV-файла [contacts.csv]: "
    ).strip() or "contacts.csv"

    try:
        with open(
            filename,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row.get("name", "").strip()

                if not name:
                    continue

                group_id = get_or_create_group(
                    cursor,
                    row.get("group", "").strip()
                )

                birthday = row.get("birthday", "").strip() or None
                email = row.get("email", "").strip() or None
                phone = row.get("phone", "").strip()
                phone_type = (
                    row.get("phone_type", "mobile")
                    .strip()
                    .lower()
                )

                cursor.execute(
                    """
                    SELECT id
                    FROM contacts
                    WHERE name = %s
                    ORDER BY id
                    LIMIT 1
                    """,
                    (name,)
                )

                existing = cursor.fetchone()

                if existing:
                    contact_id = existing[0]

                    cursor.execute(
                        """
                        UPDATE contacts
                        SET email = %s,
                            birthday = %s,
                            group_id = %s
                        WHERE id = %s
                        """,
                        (
                            email,
                            birthday,
                            group_id,
                            contact_id,
                        )
                    )

                else:
                    cursor.execute(
                        """
                        INSERT INTO contacts(
                            name,
                            email,
                            birthday,
                            group_id
                        )
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                        """,
                        (
                            name,
                            email,
                            birthday,
                            group_id,
                        )
                    )

                    contact_id = cursor.fetchone()[0]

                if phone:
                    if phone_type not in (
                        "home",
                        "work",
                        "mobile",
                    ):
                        phone_type = "mobile"

                    cursor.execute(
                        """
                        INSERT INTO phones(
                            contact_id,
                            phone,
                            type
                        )
                        VALUES (%s, %s, %s)
                        ON CONFLICT (contact_id, phone)
                        DO NOTHING
                        """,
                        (
                            contact_id,
                            phone,
                            phone_type,
                        )
                    )

        conn.commit()
        print("Импорт CSV завершён.")

    except FileNotFoundError:
        conn.rollback()
        print("CSV-файл не найден.")

    except psycopg2.Error as error:
        conn.rollback()
        print("Ошибка базы данных:", error)


def main():
    conn = connect()
    cursor = conn.cursor()

    try:
        while True:
            print("\n========== TSIS 1 PHONEBOOK ==========")
            print("1. Показать все контакты")
            print("2. Расширенный поиск")
            print("3. Фильтр по группе")
            print("4. Поиск по email")
            print("5. Сортировка")
            print("6. Пагинация")
            print("7. Добавить телефон")
            print("8. Переместить в группу")
            print("9. Экспорт в JSON")
            print("10. Импорт из JSON")
            print("11. Импорт из CSV")
            print("0. Выход")

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                show_all(cursor)

            elif choice == "2":
                search_all(cursor)

            elif choice == "3":
                filter_by_group(cursor)

            elif choice == "4":
                search_by_email(cursor)

            elif choice == "5":
                sort_contacts(cursor)

            elif choice == "6":
                pagination(cursor)

            elif choice == "7":
                add_phone(cursor, conn)

            elif choice == "8":
                move_to_group(cursor, conn)

            elif choice == "9":
                export_to_json(cursor)

            elif choice == "10":
                import_from_json(cursor, conn)

            elif choice == "11":
                import_from_csv(cursor, conn)

            elif choice == "0":
                print("До свидания!")
                break

            else:
                print("Неверный выбор.")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
from connect import connect

conn = connect()
cursor = conn.cursor()


def show_contacts():
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()

    print("\n===== Контакты =====")
    for row in rows:
        print(row)
    print("====================")


def search_contacts():
    pattern = input("Введите имя, фамилию или телефон: ")

    cursor.execute(
        "SELECT * FROM get_contacts_by_pattern(%s)",
        (pattern,)
    )

    rows = cursor.fetchall()

    if rows:
        print("\nНайдено:")
        for row in rows:
            print(row)
    else:
        print("Контакты не найдены.")


def add_or_update():
    first_name = input("Имя: ")
    last_name = input("Фамилия: ")
    phone = input("Телефон: ")

    cursor.execute(
        "CALL upsert_contact(%s,%s,%s)",
        (first_name, last_name, phone)
    )

    conn.commit()
    print("Контакт успешно добавлен или обновлен.")


def insert_many():
    n = int(input("Сколько контактов добавить? "))

    first_names = []
    last_names = []
    phones = []

    for i in range(n):
        print(f"\nКонтакт {i+1}")

        first_names.append(input("Имя: "))
        last_names.append(input("Фамилия: "))
        phones.append(input("Телефон: "))

    cursor.execute(
        "CALL insert_many_contacts(%s,%s,%s)",
        (first_names, last_names, phones)
    )

    conn.commit()
    print("Массовое добавление завершено.")


def pagination():
    limit = int(input("LIMIT: "))
    offset = int(input("OFFSET: "))

    cursor.execute(
        "SELECT * FROM get_contacts_paginated(%s,%s)",
        (limit, offset)
    )

    rows = cursor.fetchall()

    for row in rows:
        print(row)


def delete_contact():
    value = input("Введите имя или телефон: ")

    cursor.execute(
        "CALL delete_contact(%s)",
        (value,)
    )

    conn.commit()
    print("Удаление выполнено.")


while True:
    print("\n========== PHONEBOOK ==========")
    print("1. Показать все контакты")
    print("2. Поиск по шаблону")
    print("3. Добавить или обновить контакт")
    print("4. Массовое добавление")
    print("5. Показать с LIMIT/OFFSET")
    print("6. Удалить контакт")
    print("7. Выход")

    choice = input("Выберите действие: ")

    if choice == "1":
        show_contacts()

    elif choice == "2":
        search_contacts()

    elif choice == "3":
        add_or_update()

    elif choice == "4":
        insert_many()

    elif choice == "5":
        pagination()

    elif choice == "6":
        delete_contact()

    elif choice == "7":
        break

    else:
        print("Неверный выбор.")

cursor.close()
conn.close()
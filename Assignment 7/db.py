import psycopg2
import re

conn = psycopg2.connect(
    host="localhost",
    port="5434",
    database="phonebook_db",
    user="postgres",
    password="Zhanbolatuly01"
)

cursor = conn.cursor()

def input_phone():
    while True:
        phone = input("Введите телефон (+77*********): ")

        if re.fullmatch(r"\+77\d{9}", phone):
            return phone

        print("❌ Неверный формат номера!")
        print("Введите номер в формате: +77*********\n")


def show_contacts():
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()

    print("\n===== Контакты =====")

    for row in rows:
        print(row)

    print("====================\n")

def add_contact():
    first_name = input("Введите имя: ")
    last_name = input("Введите фамилию: ")
    phone = input_phone()

    cursor.execute(
        """
        INSERT INTO contacts (first_name, last_name, phone)
        VALUES (%s, %s, %s)
        """,
        (first_name, last_name, phone)
    )

    conn.commit()
    print("Контакт успешно добавлен!")

def find_contact():
    name = input("Введите имя для поиска: ")

    cursor.execute(
        """
        SELECT * FROM contacts
        WHERE first_name = %s
        """,
        (name,)
    )

    rows = cursor.fetchall()

    if rows:
        print("\nНайденные контакты:")
        for row in rows:
            print(row)
    else:
        print("Контакт не найден.")

def update_contact():
    name = input("Введите имя контакта: ")
    new_phone = input_phone()

    cursor.execute(
        """
        UPDATE contacts
        SET phone = %s
        WHERE first_name = %s
        """,
        (new_phone, name)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Контакт успешно обновлен!")
    else:
        print("Контакт не найден.")


def delete_contact():
    name = input("Введите имя контакта для удаления: ")

    cursor.execute(
        """
        DELETE FROM contacts
        WHERE first_name = %s
        """,
        (name,)
    )

    conn.commit()

    if cursor.rowcount > 0:
        print("Контакт успешно удален!")
    else:
        print("Контакт не найден.")

while True:
    print("\n===== PHONEBOOK =====")
    print("1. Показать контакты")
    print("2. Добавить контакт")
    print("3. Найти контакт")
    print("4. Изменить контакт")
    print("5. Удалить контакт")
    print("6. Выход")

    choice = input("Выберите действие: ")

    if choice == "1":
        show_contacts()

    elif choice == "2":
        add_contact()

    elif choice == "3":
        find_contact()

    elif choice == "4":
        update_contact()

    elif choice == "5":
        delete_contact()

    elif choice == "6":
        print("До свидания!")
        break

    else:
        print("Неверный выбор!")

cursor.close()
conn.close()



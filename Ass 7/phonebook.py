import csv
from connect import connect


def create_connection():
    return connect()


def insert_from_csv(filename):
    conn = create_connection()
    cur = conn.cursor()

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            cur.execute(
                "INSERT INTO contacts(name, phone) VALUES(%s,%s)",
                (row["name"], row["phone"])
            )

    conn.commit()
    cur.close()
    conn.close()


def insert_from_console():
    name = input("Name: ")
    phone = input("Phone: ")

    conn = create_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts(name, phone) VALUES(%s,%s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def show_contacts():
    conn = create_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search():
    word = input("Enter name or phone: ")

    conn = create_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT * FROM contacts
        WHERE name ILIKE %s OR phone LIKE %s
        """,
        ('%' + word + '%', '%' + word + '%')
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()


def update_contact():
    old_name = input("Enter name: ")
    new_phone = input("New phone: ")

    conn = create_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE contacts
        SET phone=%s
        WHERE name=%s
        """,
        (new_phone, old_name)
    )

    conn.commit()

    cur.close()
    conn.close()


def delete_contact():
    name = input("Enter name: ")

    conn = create_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name=%s",
        (name,)
    )

    conn.commit()

    cur.close()
    conn.close()


while True:

    print("""
1. Import CSV
2. Add contact
3. Show contacts
4. Search
5. Update
6. Delete
0. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        insert_from_csv("contacts.csv")

    elif choice == "2":
        insert_from_console()

    elif choice == "3":
        show_contacts()

    elif choice == "4":
        search()

    elif choice == "5":
        update_contact()

    elif choice == "6":
        delete_contact()

    elif choice == "0":
        break
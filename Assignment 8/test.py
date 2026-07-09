import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="Zhanbolatuly01",
    port=5434
)

cur = conn.cursor()


def test_search():
    print("\n=== Task 1: Search by Pattern ===")
    pattern = input("Enter pattern: ")
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
    rows = cur.fetchall()

    for row in rows:
        print(row)


def test_pagination():
    print("\n=== Task 2: Pagination ===")
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))

    cur.execute(
        "SELECT * FROM get_contacts_paginated(%s,%s);",
        (limit, offset)
    )

    rows = cur.fetchall()

    for row in rows:
        print(row)


def test_upsert():
    print("\n=== Task 3: Upsert Contact ===")

    first = input("First name: ")
    last = input("Last name: ")
    phone = input("Phone: ")

    cur.execute(
        "CALL upsert_contact(%s,%s,%s);",
        (first, last, phone)
    )

    conn.commit()

    print("Done!")


def test_insert_many():
    print("\n=== Task 4: Insert Many Contacts ===")

    first = ['Ali', 'John']
    last = ['A', 'B']
    phone = ['87000000001', '87000000002']

    cur.execute(
        "CALL insert_many_contacts(%s,%s,%s);",
        (first, last, phone)
    )

    conn.commit()

    print("Two contacts inserted.")


def test_delete():
    print("\n=== Task 5: Delete Contact ===")

    first = input("First name (leave empty if deleting by phone): ")
    phone = input("Phone (leave empty if deleting by name): ")

    if first == "":
        first = None

    if phone == "":
        phone = None

    cur.execute(
        "CALL delete_contact(%s,%s);",
        (first, phone)
    )

    conn.commit()

    print("Deleted.")


while True:

    print("\n========== Assignment 8 ==========")
    print("1. Search by pattern")
    print("2. Pagination")
    print("3. Upsert contact")
    print("4. Insert many contacts")
    print("5. Delete contact")
    print("0. Exit")

    choice = input("Choose: ")

    if choice == "1":
        test_search()

    elif choice == "2":
        test_pagination()

    elif choice == "3":
        test_upsert()

    elif choice == "4":
        test_insert_many()

    elif choice == "5":
        test_delete()

    elif choice == "0":
        break

    else:
        print("Wrong choice!")

cur.close()
conn.close()
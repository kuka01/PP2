import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="Zhanbolatuly01",
    port=5434
)

cur = conn.cursor()

print("=" * 50)
print("ASSIGNMENT 8 TEST")
print("=" * 50)

# -----------------------------
# TASK 1
# -----------------------------
print("\n1. Search by pattern")

cur.execute("SELECT * FROM get_contacts_by_pattern('777')")
rows = cur.fetchall()

for row in rows:
    print(row)

# -----------------------------
# TASK 2
# -----------------------------
print("\n2. Pagination")

cur.execute("SELECT * FROM get_contacts_paginated(5,0)")
rows = cur.fetchall()

for row in rows:
    print(row)

# -----------------------------
# TASK 3
# -----------------------------
print("\n3. Upsert")

cur.execute("""
CALL upsert_contact(
'Test',
'User',
'87001112233'
)
""")
conn.commit()

cur.execute("""
SELECT *
FROM contacts
WHERE first_name='Test'
""")

print(cur.fetchall())

# -----------------------------
# TASK 4
# -----------------------------
print("\n4. Insert many")

cur.execute("""
CALL insert_many_contacts(
ARRAY['AAA','BBB'],
ARRAY['One','Two'],
ARRAY['87000000001','87000000002']
)
""")

conn.commit()

cur.execute("""
SELECT *
FROM contacts
WHERE first_name IN ('AAA','BBB')
""")

print(cur.fetchall())

# -----------------------------
# TASK 5
# -----------------------------
print("\n5. Delete")

cur.execute("""
CALL delete_contact(
'AAA',
NULL
)
""")

conn.commit()

cur.execute("""
SELECT *
FROM contacts
WHERE first_name='AAA'
""")

print(cur.fetchall())

cur.close()
conn.close()

print("\nAll tests completed successfully!")
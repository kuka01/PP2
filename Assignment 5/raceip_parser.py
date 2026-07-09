import re

with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("========== RECEIPT ==========\n")

# -----------------
# Prices
# -----------------

prices = re.findall(r"\d+\.\d{2}", text)

print("Prices:")

for p in prices:
    print(p)

# -----------------
# Total
# -----------------

total = sum(float(price) for price in prices)

print("\nTotal:", total)

# -----------------
# Date
# -----------------

date = re.search(r"\d{2}[./-]\d{2}[./-]\d{4}", text)

if date:
    print("\nDate:", date.group())

# -----------------
# Time
# -----------------

time = re.search(r"\d{2}:\d{2}(:\d{2})?", text)

if time:
    print("Time:", time.group())

# -----------------
# Payment
# -----------------

payment = re.search(r"(Cash|Card|Visa|MasterCard)", text, re.IGNORECASE)

if payment:
    print("Payment:", payment.group())

# -----------------
# Product names
# -----------------

print("\nProducts:")

products = re.findall(r"[A-Za-zА-Яа-я ]+(?=\s+\d+\.\d{2})", text)

for product in products:
    print(product.strip())
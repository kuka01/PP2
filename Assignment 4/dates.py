from datetime import datetime, timedelta, timezone

print("Current Date and Time")

now = datetime.now()

print(now)

print("\nCreate Date Object")

birthday = datetime(2005, 8, 20)

print(birthday)

print("\nDate Formatting")

print(now.strftime("%d/%m/%Y"))
print(now.strftime("%A"))
print(now.strftime("%H:%M:%S"))

print("\nTime Difference")

difference = now - birthday

print("Days:", difference.days)

print("\nAdd 30 Days")

future = now + timedelta(days=30)

print(future)

print("\nTimezone")

utc = datetime.now(timezone.utc)

print(utc)
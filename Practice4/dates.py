from datetime import datetime, timedelta

# Task 1: subtract 5 days from current date
today = datetime.now()
five_days_ago = today - timedelta(days=5)
print("Task 1 — five days ago:", five_days_ago.date())

# Task 2: yesterday, today, tomorrow
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print("\nTask 2:")
print("Yesterday:", yesterday.date())
print("Today:    ", today.date())
print("Tomorrow: ", tomorrow.date())

# Task 3: drop microseconds from datetime
now = datetime.now()
print("\nTask 3 — original:    ", now)
print("Task 3 — no microseconds:", now.replace(microsecond=0))

# Task 4: difference between two dates in seconds
date1 = datetime(2025, 1, 1, 12, 0, 0)
date2 = datetime(2025, 1, 2, 12, 0, 0)
diff = date2 - date1
print("\nTask 4 — difference in seconds:", diff.total_seconds())

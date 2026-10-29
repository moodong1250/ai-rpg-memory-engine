import sqlite3

conn = sqlite3.connect("rpg.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, action, target, kill_count, exp_gain
FROM events
ORDER BY id DESC
""")

events = cursor.fetchall()

for event in events:
    print(event)

conn.close()
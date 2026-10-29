import sqlite3

conn = sqlite3.connect("rpg.db")
cursor = conn.cursor()

monster = input("조회할 몬스터: ")

cursor.execute(
    """
    SELECT SUM(kill_count)
    FROM events
    WHERE target = ? AND action = 'hunt'
    """,
    (monster,)
)

total_kills = cursor.fetchone()[0]

conn.close()

if total_kills is None:
    total_kills = 0

print(f"{monster} 총 처치 수: {total_kills}마리")
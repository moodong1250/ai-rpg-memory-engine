import sqlite3

conn = sqlite3.connect("rpg.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    action TEXT NOT NULL,
    target TEXT,
    kill_count INTEGER DEFAULT 0,
    exp_gain INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
INSERT OR IGNORE INTO player (id, exp)
VALUES (1, 0)
""")

conn.commit()
conn.close()

print("플레이어 DB 생성 완료")
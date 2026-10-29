import sqlite3


def get_monster_kills(monster):

    conn = sqlite3.connect("rpg.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(kill_count)
        FROM events
        WHERE target = ?
        AND action = 'hunt'
        AND player_id = ?
        """,
        (monster, 1)
    )

    total_kills = cursor.fetchone()[0]

    conn.close()

    if total_kills is None:
        total_kills = 0

    return total_kills
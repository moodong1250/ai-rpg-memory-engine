import os
import json
import random
import sqlite3

from memory import get_monster_kills
from pathlib import Path

from dotenv import load_dotenv
from google import genai

load_dotenv(Path(__file__).with_name(".env"))

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

player_exp = 0

conn = sqlite3.connect("rpg.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT exp FROM player WHERE id = ?",
    (1,)
)

player_exp = cursor.fetchone()[0]

conn.close()

print("불러온 경험치:", player_exp)

monster_exp = {
    "고블린": (5, 10),
    "슬라임": (2, 5),
    "늑대": (7, 12),
    "오크": (15, 25)
}

while True:


    mode = input("\n모드 선택 (1: 행동, 2: 처치 조회, exit: 종료): ").strip().lower()


    if mode == "exit":
        print("게임을 종료합니다.")
        break

    if mode == "2":

        monster = input("조회할 몬스터: ")

        total = get_monster_kills(monster)

        print(f"지금까지 {monster}을(를) {total}마리 처치했습니다.")
        continue

    if mode != "1":
        print("올바른 모드를 선택해주세요.")
        continue

    user_input = input("행동을 입력하세요: ")


    prompt = f"""
    너는 RPG 행동 분석기다.

    사용자의 행동을 분석해서 JSON 형식으로만 답해라.

    제공된 DB의 기록만 근거로 답해라.

    category는 반드시 아래 중 하나:
    - combat
    - exploration
    - social

    action은 아래처럼 영어 내부 명령어로 정리:
    - hunt
    - travel
    - talk
    - meet


    target:
    행동의 대상. 몬스터라면 종류를 추출한다.

    kill_count:
    명확하게 처치했다고 서술한 몬스터의 수.
    처치 수가 명시되지 않았으면 0으로 설정한다.
    사냥 기간으로 처치 수를 추정하지 않는다.

    duration_days는 행동 기간을 일(day) 단위 숫자로 변환

    사용자 입력:
    {user_input}

    반드시 아래 JSON 형식으로만 답해라.

    {{
    "category": "",
    "action": "",
    "target": "",
    "kill_count": 0
    }}
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )


    result = json.loads(response.text)

    if result["action"] == "hunt":

        monster = result["target"]
        kill_count = result["kill_count"]

    if monster in monster_exp and kill_count > 0:

        min_exp, max_exp = monster_exp[monster]

        exp_gain = 0

        for i in range(kill_count):
            exp_gain += random.randint(min_exp, max_exp)

        player_exp += exp_gain

        conn = sqlite3.connect("rpg.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE player SET exp = ? WHERE id = ?",
            (player_exp, 1)
        )

        cursor.execute(
            """
            INSERT INTO events (
                player_id,
                category,
                action,
                target,
                kill_count,
                exp_gain
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                result["category"],
                result["action"],
                monster,
                kill_count,
                exp_gain
            )
        )

        conn.commit()
        conn.close()

        print("처치 몬스터:", monster)
        print("처치 수:", kill_count)
        print("획득 경험치:", exp_gain)
        print("현재 경험치:", player_exp)

    else:
        print("처치 수가 없거나 등록되지 않은 몬스터입니다.")

    print(result)

    print("category:", result["category"])
    print("action:", result["action"])
    print("target:", result["target"])
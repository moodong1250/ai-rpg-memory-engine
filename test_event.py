from event_system import load_events, get_random_event

events = load_events()
current_region = "초보자의 숲"

selected = get_random_event(events, current_region)

if selected is not None:

    # 문제 1. 이벤트 제목 출력
    print(selected["title"])

    # 문제 2. 이벤트 설명 출력
    print(selected["description"])

    # 문제 3. 선택지 3개 출력
    for number, choice in enumerate(selected["choices"], start=1):
        print(f"{number}. {choice}")



    user_choice = int(input("행동을 선택하세요: "))

    choices = selected["choices"]

    # 입력한 번호가 실제 선택지 범위에 있는지 확인
    if 1 <= user_choice <= len(choices):

        action = choices[user_choice - 1]
        print("선택한 행동:", action)

    else:
        print("잘못된 선택입니다.")

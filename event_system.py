import json
import random




def load_events():
    with open('events.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data


def get_random_event(events, current_region):

    # 1. 현재 지역에 해당하는 이벤트 추출
    region_events = [
        event for event in events
        if event["region"] == current_region
    ]

    # 2. 해당 지역에 이벤트가 없다면 종료
    if not region_events:
        return None

    # 3. 해당 지역 이벤트들의 가중치 추출
    weights = [event["weight"] for event in region_events]

    # 4. 가중치에 따라 이벤트 선택
    selected = random.choices(
        population=region_events,
        weights=weights,
        k=1
    )[0]

    return selected


"""실습 1 | 같은 설명에 맞는 상자가 여러 개라면 (교안 4·19·22쪽)

입력: 위치 이름, 색, 선택적으로 사용자가 알려 준 위치 단서.
처리: 지도 확인 → 현재 관측에서 후보 찾기 → 후보 수에 따라 분기.
출력: 상태 이름과 물체 ID 또는 사용자에게 보여 줄 안내.
"""

# 관측 시각이 같다고 가정한 작업대 배치. 창가와 입구에 빨간 상자가 하나씩 있다.
PLACES = {"A", "B", "D"}
OBJECTS = [
    {"id": "box_01", "place": "A", "color": "빨간색", "side": "입구"},
    {"id": "box_02", "place": "A", "color": "빨간색", "side": "창가"},
]


def resolve(place, color, side=None):
    """사용자가 말한 특징을 현재 관측과 대조한다."""
    if place not in PLACES:
        return "unknown_target", f"지도에서 {place} 위치를 찾을 수 없습니다."

    # 위치 단서는 두 번째 대화에서 들어온다. 첫 요청에서는 위치와 색만 비교한다.
    candidates = [
        obj for obj in OBJECTS
        if obj["place"] == place and obj["color"] == color
        and (side is None or obj["side"] == side)
    ]
    if not candidates:
        return "not_observed", "일치하는 상자가 보이지 않습니다. 작업대를 다시 관측하세요."
    if len(candidates) > 1:
        options = ", ".join(obj["side"] for obj in candidates)
        return "clarification_required", f"어느 쪽 상자인가요? 후보는 {options}입니다."
    return "resolved", candidates[0]["id"]


if __name__ == "__main__":
    # 자연어 이해기가 이미 추출한 인수를 넣는다. 이 예제에는 LLM 호출이 없다.
    for request in [("A", "빨간색"), ("A", "빨간색", "창가"), ("Z", "빨간색"), ("A", "파란색")]:
        status, detail = resolve(*request)
        print(f"{request} → {status} | {detail}")

"""실습 4 | 명령 전송 후 관측에 따라 다음 작업 고르기 (교안 6~7·15~16·24쪽)

입력: 로봇 위치, 대상 상자의 파지 여부, B의 빈자리 관측값.
처리: 현재 작업의 사전조건을 대조한다. None은 아직 확인하지 못했다는 뜻이다.
출력: 다음 행동 또는 보류 이유. 각 행은 독립된 모의 관측 장면이다.
"""


def next_action(location, holding_box, free_b):
    """A에서 대상 상자를 집어 B에 놓는 구간의 다음 행동 하나를 정한다."""
    # 명령을 전송했다는 사실만으로 holding_box를 True로 바꾸지 않는다.
    if holding_box is None:
        return "손과 대상 상자를 다시 관측"
    if not holding_box:
        if location == "A":
            return "A에서 상자 자세를 다시 측정한 뒤 집기"
        return "상자 위치를 확인하고 운반 계획 다시 세우기"

    # 파지를 확인한 뒤에야 차체가 B로 이동할 수 있다.
    if location != "B":
        return "상자를 들고 B로 이동"

    # None과 False를 따로 처리한다. 둘을 합치면 센서 가림과 실제 점유를 혼동한다.
    if free_b is None:
        return "손에 든 채 B를 다시 관측"
    if not free_b:
        return "놓기를 보류하고 대기 또는 목적지 변경 문의"
    return "B에 놓기 명령 전송 후 상자 위치와 빈손 확인"


if __name__ == "__main__":
    # 예측 먼저: 각 장면에서 move, pick, place 중 무엇이 아직 허용되지 않는가?
    scenes = [
        ("집기 명령만 전송", "A", None, None),
        ("상자가 탁자에 남음", "A", False, None),
        ("파지 확인", "A", True, None),
        ("B 카메라 가림", "B", True, None),
        ("B에 다른 물체가 있음", "B", True, False),
        ("B 빈자리 확인", "B", True, True),
    ]
    for event, location, holding_box, free_b in scenes:
        print(f"{event} → {next_action(location, holding_box, free_b)}")

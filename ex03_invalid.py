"""실습 3 | 오타와 순환은 어떻게 다른가? (교안 11·21·23쪽)

입력: 실습 2의 정상 계획과 선행 관계 한 곳을 바꾼 복사본 두 개.
처리: 같은 검증 함수에 세 계획을 넣고 오류 종류와 근거를 기록한다.
출력: 정상 순서, 순환 경로, 미등록 ID.
"""
from graphlib import CycleError
from ex02_graph import PLAN, ready_groups


def diagnose(label, plan):
    """오류가 난 계획을 실행하지 않고 원인을 출력한다."""
    try:
        groups = list(ready_groups(plan))
    except CycleError as error:
        # CycleError는 ValueError의 하위 클래스이므로 더 구체적인 오류부터 처리한다.
        # args[1]에는 시작과 끝이 같은 실제 순환 경로가 들어 있다.
        print(label, "| 순환:", " → ".join(error.args[1]))
    except ValueError as error:
        print(label, "|", error)
    else:
        print(label, "| 정상:", " → ".join("/".join(group) for group in groups))


if __name__ == "__main__":
    # 새 딕셔너리를 만들어 실험한다. 정상 계획을 다음 실행에서도 재사용할 수 있다.
    diagnose("원본", PLAN)
    diagnose("잘못된 대기", {**PLAN, "A": ("place",)})
    diagnose("이름 오타", {**PLAN, "place": ("B", "chek")})

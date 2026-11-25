"""실습 2 | 실행 가능한 작업 순서 구하기 (교안 8~10·19~20쪽)

입력: 작업 ID → 바로 앞에서 끝나야 하는 작업 ID들의 튜플.
처리: 선행 ID 검증 → 위상 정렬 준비 → 준비된 작업을 차례로 완료 처리.
출력: 각 단계에서 선행 조건이 풀린 작업들. 실제 장비 명령은 보내지 않는다.
"""
from graphlib import TopologicalSorter

# A, B, D는 각각 '해당 위치로 이동하는 작업'의 짧은 ID다.
PLAN = {
    "A": (),
    "check": (),             # 독립된 고정 카메라로 B 공간을 조회한다.
    "pick": ("A",),          # 항목 하나인 튜플은 쉼표가 필요하다.
    "B": ("pick",),
    "place": ("B", "check"),  # B 도착과 공간 조회가 모두 끝나야 한다.
    "D": ("place",),
    "charge": ("D",),
}


def ready_groups(plan):
    """같은 단계에서 시작 가능한 작업들을 한 묶음씩 돌려준다."""
    # graphlib는 선행 목록에만 있는 이름도 노드로 받아들인다.
    # 'chek' 같은 오타가 별도 작업으로 실행되지 않도록 먼저 검사한다.
    referenced = {parent for parents in plan.values() for parent in parents}
    missing = referenced.difference(plan)
    if missing:
        raise ValueError("미등록 선행 ID: " + ", ".join(sorted(missing)))

    graph = TopologicalSorter(plan)
    graph.prepare()  # 순환이 있으면 한 작업도 출력하기 전에 CycleError가 발생한다.
    while graph.is_active():
        ready = graph.get_ready()
        yield ready
        # 이 실습에서는 묶음 안의 모든 작업이 성공했다고 가정한다.
        # 실물에서는 작업별 성공 관측을 받은 뒤에만 done을 호출해야 한다.
        graph.done(*ready)


if __name__ == "__main__":
    for step, group in enumerate(ready_groups(PLAN), start=1):
        print(f"{step}단계: {', '.join(group)}")

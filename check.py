# check.py  —  네 가지 상황을 모든 버전에 똑같이 먹여 봅니다
# ---------------------------------------------------------------------------
# 쓰는 법
#     python check.py
#     (인자 없이 실행하면 v0~v5를 모두 검사합니다.)
#
#     python3 check.py v0_plain
#     python3 check.py v1_security
#     python3 check.py v4_final
#     python3 check.py v5_review
#
#   (같은 폴더에 그 이름의 .py 파일이 있어야 하고,
#    그 안에 load_scores(path) 함수가 있어야 합니다.)
#
# 이 파일은 8주차 test_fixed.py 와 같은 방식입니다.
#   "죽지 않는다"는 "맞다"가 아닙니다.
#   네 상황에서 각각 무엇을 돌려주는지, 무엇을 알려 주는지를 눈으로 보세요.
# ---------------------------------------------------------------------------

import sys
import importlib.util
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
VERSION_DIR = SCRIPT_DIR / "week10_files"
VERSIONS = [
    "v0_plain",
    "v1_security",
    "v2_analyst",
    "v3_perf",
    "v4_final",
    "v5_review",
]

CASES = [
    ("없는파일.csv", "파일이 없을 때"),
    ("scores.csv",   "정상 파일 (지저분한 줄이 섞여 있음)"),
    ("empty.csv",    "헤더만 있고 내용이 없을 때"),
    ("weird.csv",    "점수가 1000점, 빈 칸, 공백, 중복 이름"),
]


def check_version(name):
    module_path = VERSION_DIR / f"{name}.py"
    if not module_path.is_file():
        print(f"'{module_path}' 파일을 찾을 수 없습니다.")
        return

    spec = importlib.util.spec_from_file_location(name, module_path)
    if spec is None or spec.loader is None:
        print(f"'{module_path}' 파일을 불러올 수 없습니다.")
        return

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if not hasattr(mod, "load_scores"):
        print(f"'{name}.py' 안에 load_scores 함수가 없습니다.")
        return

    load_scores = mod.load_scores

    print("=" * 68)
    print(f"  {name}.py  검사")
    print("=" * 68)

    for filename, why in CASES:
        path = SCRIPT_DIR / filename
        print(f"\n[{why}]  {filename}")
        try:
            result = load_scores(str(path))
        except Exception as e:
            print(f"  → 예외: {type(e).__name__}: {e}")
            continue

        print(f"  → 돌려준 값의 종류: {type(result).__name__}")
        try:
            print(f"  → 길이: {len(result)}")
        except TypeError:
            pass
        text = repr(result)
        print(f"  → 내용: {text[:200]}{' ...' if len(text) > 200 else ''}")

    print("\n" + "-" * 68)
    print("판정표에 옮겨 적으세요")
    print("  1. 네 상황 중 몇 개를 '제대로' 처리했나요?")
    print("  2. 오류 없이 틀린 답을 준 경우(조용한 실패)가 몇 번인가요?")
    print("     - 105점이 그대로 들어갔다면 조용한 실패입니다.")
    print("     - 빈 점수를 0점으로 바꿨다면 그것도 조용한 실패입니다.")
    print("  3. 건너뛴 줄을 사용자에게 알려 주나요?")
    print("  4. 함수 하나가 20줄 이내인가요? (5주차 기준)")
    print("-" * 68)


def main():
    names = sys.argv[1:] or VERSIONS
    for name in names:
        check_version(name.replace(".py", ""))


if __name__ == "__main__":
    main()
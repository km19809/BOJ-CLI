from typing import NamedTuple
from itertools import zip_longest
from pathlib import Path
from sys import stderr
from colors import RESET, RED, GREEN, YELLOW,CYAN_BG, MAGENTA_BG


def handle_argument(args: NamedTuple) -> None:
    """
    args를 분해해 run에 전달하는 단순한 함수.
    """
    run(str(args.problem), args.verbose)


def run(problem: str, verbose: bool):
    """
    problem번 폴더의 output*.txt와 그에 대응하는 result*.txt를 이용해 예제를 채점.\n
    verbose가 True이면 채점 중에 각 파일의 채점 결과를 표시함.
    """
    problem_path = Path(f'./{problem}')
    examples = problem_path.glob(f'output*.txt')
    total = 0
    wrong = []
    for example_path in examples:
        total += 1
        result_name = example_path.name.replace("output", "result")
        result_path = (problem_path/result_name)
        if result_path.exists() and result_path.is_file():
            with example_path.open(encoding='UTF-8') as e:
                with result_path.open(encoding='UTF-8') as r:
                    for line_number, (example, result) in enumerate(zip_longest(e, r, fillvalue='')):
                        example = example.rstrip()
                        result = result.rstrip()
                        if example != result:
                            wrong.append(
                                (str(example_path), f"{line_number+1}번째 줄: `{MAGENTA_BG}{example}{RESET}`!=`{CYAN_BG}{result}{RESET}`"))
                            if verbose:
                                print(f"{RED}✗{RESET} {example_path}")
                            break
                    else:
                        if verbose:
                            print(f"{GREEN}✓{RESET} {example_path}")
        else:
            wrong.append(
                (str(example_path), f"채점 불가: {result_name}이 존재하지 않음."))
            if verbose:
                print(f"{RED}✗{RESET} {example_path}")
    if total == 0:
        print(f"{problem_path}번 문제: {RED}예제 출력이 없습니다!{RESET}",  file=stderr)
        return
    correct_count = total-len(wrong)
    correct_rate = correct_count/total
    decoration = GREEN if correct_rate > 0.66 else (
        YELLOW if correct_rate > 0.33 else RED)
    print(
        f"정답률: {correct_count}/{total} {decoration}{correct_rate*100:.1f}{RESET}%\n")
    print("틀린 항목:")
    if len(wrong) > 0:
        for w in wrong:
            print(*w)
    else:
        print(
            f"{RED}~{YELLOW}*{GREEN}~{RESET} 틀린 예제가 없어요! {GREEN}~{YELLOW}*{RED}~{RESET}")

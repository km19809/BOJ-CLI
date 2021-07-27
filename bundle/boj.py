"""
Gist에서 활용하기 위해 단일 파일로 만든 BOJ 모듈.
표준 라이브러리 이외의 어떤 것도 활용하지 않음.
파일이름으로 Main을 사용하는 신규 모듈.
Author: Minsoo Kim<km19809@users.noreply.github.com>
"""
import json
import re
import subprocess
import urllib.request as req
from itertools import zip_longest
from pathlib import Path
from shutil import copyfile
from sys import stderr
from typing import NamedTuple


# ANSI Colors
RESET = "\x1b[0m"
RED = "\x1b[31m"
GREEN = "\x1b[32m"
YELLOW = "\x1b[33m"

MAGENTA_BG = "\x1b[45m"
CYAN_BG = "\x1b[46m"

# Build Command
commands = {'c': {'build': 'gcc Main.c -o Main -O2 -Wall -lm -static -DONLINE_JUDGE -DBOJ', 'run': './Main'},
            'cc': {'build': 'g++ Main.cc -o Main -O2 -Wall -lm -static -DONLINE_JUDGE -DBOJ', 'run': './Main'},
            'cpp': {'build': 'g++ Main.cc -o Main -O2 -Wall -lm -static -DONLINE_JUDGE -DBOJ', 'run': './Main'},
            'cs': {'build': 'dotnet new console --force -o Main && dotnet publish Main --configuration Release --self-contained true --runtime linux-x64', 'run': './Main'},
            'go': {'build': 'go build Main.go', 'run': './Main'},
            'java': {'build': 'javac -J-Xms1024m -J-Xmx1920m -J-Xss512m -encoding UTF-8 Main.java', 'run': 'java -Xms1024m -Xmx1920m -Xss512m -Dfile.encoding=UTF-8 Main'},
            'js': {'build': None, 'run': 'node Main.js'},
            'kt': {'build': 'kotlinc-jvm -J-Xms1024m -J-Xmx1920m -J-Xss512m -include-runtime -d Main.jar Main.kt', 'run': 'java -Xms1024m -Xmx1920m -Xss512m -Dfile.encoding=UTF-8 -XX:+UseSerialGC -DONLINE_JUDGE=1 -DBOJ=1 -jar Main.jar'},
            'pl': {'build': 'perl -c Main.pl', 'run': 'perl Main.pl'},
            'py': {'build': 'python -c "import py_compile; py_compile.compile(r\'Main.py\')"', 'run': 'python Main.py'},
            'rs': {'build': 'rustc --edition 2018 -O -o Main Main.rs', 'run': './Main'},
            'vb': {'build': 'dotnet new console --language "VB"--force -o Main && dotnet publish Main --configuration Release --self-contained true --runtime linux-x64', 'run': './Main'}}


def get(args: NamedTuple) -> None:
    """
    문제번호를 이름으로 하는 폴더를 생성,\n
    BOJ 문제를 HTML형태로 저장하고, 입력과 출력 예제를 생성함.\n
    추가로 소스코드가 존재하지 않을 경우 소스코드를 templates폴더를 바탕으로 생성함.
    """
    problem = args.problem
    lang = args.language
    html = req.urlopen(
        f"https://www.acmicpc.net/problem/{problem}").read().decode('UTF-8')
    matches = re.findall(
        r'<pre +class="sampledata" +id="sample-((?:input|output)-\d+)">([^<>]+)</pre>', html)
    problem_path = Path(f"./{problem}")
    problem_path.mkdir(exist_ok=True)
    for match in matches:
        with (problem_path/f"{match[0]}.txt").open('w', encoding="UTF-8") as out:
            out.write(match[1].replace("\r\n", "\n"))
    with (problem_path/f"{problem}.html").open('w', encoding="UTF-8") as problem_out:
        problem_out.write(html.replace("\r\n", "\n"))
    template_path = Path(f"./templates/template.{lang}")
    dest_path = problem_path/f"Main.{lang}"
    if not dest_path.exists():
        print("소스코드가 발견되지 않았습니다.")
        if template_path.exists() and template_path.is_file():
            print(f"틀({template_path})을 사용합니다.")
            copyfile(template_path, dest_path)
        else:
            print(f"틀({template_path})이 없습니다. 빈 파일을 생성합니다.")
            dest_path.open('w').close()
    print("다운로드 완료")


def run_test(command: list, example: Path, write_to_file: bool):
    """
    command를 바탕으로 프로세스를 생성, example의 내용을 UTF-8로 표준 입력에 입력시킴.\n
    write_to_file이 True이면 실행결과를 result*.txt에 저장함.
    """
    print(f"{YELLOW}입력{RESET}: {example.name}")
    with example.open(encoding='UTF-8') as f:
        result = subprocess.run(
            command, input=f.read(), encoding='UTF-8', capture_output=True, cwd=example.parent,shell=True)
    print(result.stdout, end='')
    if result.stderr:
        print(f"{RED}오류 발생!\n{result.stderr}\n{RESET}", file=stderr)
    elif write_to_file:
        with open(str(example).replace("input", "result"), 'w', encoding='UTF-8') as result_file:
            result_file.write(result.stdout)


def run(problem: str, lang: str, write_to_file: bool, command_dict:dict):
    """
    problem 폴더에서 소스코드를 빌드 및 실행.\n
    lang은 실행할 소스코드의 확장자.\n
    options는 인터프리터/컴파일러에 옵션으로 사용됨.\n
    write_to_file이 True이면 실행결과를 result*.txt에 저장함.
    """
    problem_path = Path(f'./{problem}')
    examples = problem_path.glob(f'input*.txt')
    file_extension=lang.split('.')[-1] # c99.c등 특수 사례를 구분
    input_file = problem_path / f'Main.{file_extension}'
    if not input_file.exists():
        print(f"{input_file}:{RED} 대상 파일이 존재하지 않습니다.{RESET}",  file=stderr)
        return
    elif input_file.is_dir():
        print(f"{input_file}:{RED} 디렉터리입니다.{RESET}",  file=stderr)
        return
    if lang in command_dict:
        build_command=command_dict[lang]["build"].format(input_file=input_file)
        run_command=command_dict[lang]["run"].format(input_file=input_file)
        if build_command is not None:
            print(f"{YELLOW}빌드{RESET}: {build_command}")
            try:
                subprocess.run(build_command, check=True, capture_output=True, cwd=problem_path, shell=True)
            except subprocess.CalledProcessError as e:
                print(f"{RED}빌드 실패!{RESET}\n명령어: {e.cmd}\n\
                    표준 출력:\n{e.stdout.decode('UTF-8')}\n{RED}표준 오류{RESET}:\n{e.stderr.decode('UTF-8')}",
                    file=stderr, sep='\n')
                return
        else:
            print(f"{GREEN}빌드 성공!{RESET}")
        print(f"{YELLOW}실행{RESET}: {run_command}")
        for example in examples:
            run_test(run_command, example, write_to_file)
    else:
        print(f"{lang}:{RED} 지원되지 않는 언어입니다.{RESET}",  file=stderr)


def check(problem: str, verbose: bool):
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
                (str(example_path), f"결과 파일({result_name})이 없습니다."))
            if verbose:
                print(f"{RED}✗{RESET} {example_path}")
    if total == 0:
        print(f"{problem_path}번 문제: {RED}결과와 비교할 예제 출력이 없습니다!{RESET}",  file=stderr)
        return
    correct_count = total-len(wrong)
    correct_rate = correct_count/total
    decoration = GREEN if correct_rate > 0.66 else (
        YELLOW if correct_rate > 0.33 else RED)
    print(
        f"{YELLOW}정답률{RESET}: {correct_count}/{total} {decoration}{correct_rate*100:.1f}{RESET}%")
    if len(wrong) > 0:
        print(f"{YELLOW}오답{RESET}:")
        for w in wrong:
            print(f"{w[0]} > {w[1]}")
    else:
        print(
            f"{RED}~{YELLOW}*{GREEN}~{RESET} 예제를 모두 맞췄어요! {GREEN}~{YELLOW}*{RED}~{RESET}")


def handle_run_argument(args: NamedTuple) -> None:
    """
    args를 분해해 run에 전달하는 함수.
    """
    cmds=commands
    if args.commands:
        cmds=json.load(Path(args.commands).open())
    run(str(args.problem), args.language, args.write_result,cmds)
    if args.check:
        check(str(args.problem),False)


def handle_check_argument(args: NamedTuple) -> None:
    """
    args를 분해해 check에 전달하는 단순한 함수.
    """
    check(str(args.problem), args.verbose)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog="boj",  description="백준 온라인 저지 비공식 보조도구\n예제를 다운로드하고, 작성한 코드를 실행 및 채점합니다.")
    subparsers = parser.add_subparsers(help='하위 명령어')

    parser_get = subparsers.add_parser("get", help="예제 입력과 출력을 다운로드합니다.")
    parser_get.add_argument("problem", type=int, help="문제 번호")
    parser_get.add_argument("-l", "--language", default="py",
                            help="사용할 프로그래밍 언어 확장자. 틀 `templates/template.*`이 없으면 빈 파일을 생성합니다. (기본값: %(default)s)")
    parser_get.set_defaults(func=get)

    parser_run = subparsers.add_parser(
        "run", help="작성한 프로그램을 실행합니다. 결과를 파일`result*.txt`에 작성합니다.")
    parser_run.add_argument("problem", type=int, help="문제 번호")
    parser_run.add_argument("-l", "--language",  default="py",
                            help="사용한 프로그래밍 언어 확장자. (기본값: %(default)s)")
    parser_run.add_argument("-n", "--no_result",  action="store_false", dest="write_result",
                            help="사용 시, 실행만 하고 결과 파일을 저장하지 않습니다.")
    parser_run.add_argument("-c", "--commands",  nargs='?',
                            help="빌드 및 실행 명령어를 담은 json 설정 파일을 불러옵니다.")
    parser_run.add_argument("--check",  action="store_true",
                            help="실행 후 바로 채점합니다.")
    parser_run.add_argument("options", default=[],
                            nargs='*', help="빌드 시 옵션을 설정합니다.")
    parser_run.set_defaults(func=handle_run_argument)

    parser_check = subparsers.add_parser("check", help="예제를 기반으로 채점합니다.")
    parser_check.add_argument("problem", type=int, help="문제 번호")
    parser_check.add_argument(
        "-v", "--verbose",  action="store_true", help="사용 시, 맞은 파일도 표시합니다.")
    parser_check.set_defaults(func=handle_check_argument)

    args = parser.parse_args()
    args.func(args)

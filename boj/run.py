import json
import subprocess
from typing import NamedTuple
from pathlib import Path
from sys import  stderr
from colors import RESET, RED, GREEN, YELLOW
from check import check

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



def handle_argument(args: NamedTuple) -> None:
    """
    args를 분해해 run에 전달하는 함수.
    """
    cmds=commands
    if args.commands:
        cmds=json.load(Path(args.commands).open())
    run(str(args.problem), args.language, args.write_result,cmds)
    if args.check:
        check(str(args.problem),False)

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
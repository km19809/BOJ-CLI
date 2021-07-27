import subprocess
from typing import NamedTuple
from pathlib import Path
from sys import  stderr
from colors import RESET, RED, GREEN, YELLOW
interpreter = {
    "sh": "bash {input_file}",
    "js": "node {input_file}",
    "lua": "lua {input_file}",
    "pl": "perl {input_file}",
    "py": "python {input_file}",
    "rb": "ruby {input_file}",
}
compiler = {
    "c": {"build":"gcc {input_file} -o {output_file}", "run": "{output_file}"},
    "cpp": {"build":"g++ {input_file} -o {output_file}", "run": "{output_file}"},
    "go": {"build":"go build {input_file} -o {output_file}", "run": "{output_file}"},
    "hs": {"build":"ghc {input_file} -o {output_file}", "run": "{output_file}"},
    "rs": {"build":"rustc {input_file} -o {output_file}", "run": "{output_file}"},
    "ts": {"build":"tsc {input_file}", "run": "node {output_file}.js"},
}


def handle_argument(args: NamedTuple) -> None:
    """
    args를 분해해 run에 전달하는 단순한 함수.
    """
    run(str(args.problem), args.language, args.options, args.write_result)


def run_test(command: list, example: Path, write_to_file: bool):
    """
    command를 바탕으로 프로세스를 생성, example의 내용을 UTF-8로 표준 입력에 입력시킴.\n
    write_to_file이 True이면 실행결과를 result*.txt에 저장함.
    """
    print(f"예제 {example.name}에 대한 출력:")
    with example.open(encoding='UTF-8') as f:
        result = subprocess.run(
            command, input=f.read(), encoding='UTF-8', capture_output=True)
    print(result.stdout, end='')
    if result.stderr:
        print(f"{RED}오류 발생!\n{result.stderr}\n{RESET}", file=stderr)
    elif write_to_file:
        with open(str(example).replace("input","result"),'w',encoding='UTF-8') as result_file:
            result_file.write(result.stdout)
        


def run(problem: str, lang: str, options: list, write_to_file: bool):
    """
    problem 폴더에서 소스코드를 빌드 및 실행.\n
    lang은 실행할 소스코드의 확장자.\n
    options는 인터프리터/컴파일러에 옵션으로 사용됨.\n
    write_to_file이 True이면 실행결과를 result*.txt에 저장함.
    """
    problem_path = Path(f'./{problem}')
    examples = problem_path.glob(f'input*.txt')
    input_file = problem_path / f'{problem}.{lang}'
    output_file = problem_path / f'{problem}'
    if not input_file.exists():
        print(f"{input_file}:{RED} 대상 파일이 존재하지 않습니다.{RESET}",  file=stderr)
        return
    elif input_file.is_dir():
        print(f"{input_file}:{RED} 디렉터리입니다.{RESET}",  file=stderr)
        return
    if lang in interpreter:
        raw_command = interpreter[lang].format(
            input_file=input_file, output_file=output_file)
        print(f"{YELLOW}실행:{RESET} {raw_command}{' '.join(options)}\n")
        command = raw_command.split()+options
        for example in examples:
            run_test(command, example, write_to_file)
    elif lang in compiler:
        try:
            raw_build_command = compiler[lang]["build"].format(
                input_file=input_file, output_file=output_file)
            print(f"{YELLOW}컴파일:{RESET} {raw_build_command}")
            build_command = raw_build_command.split()+options
            subprocess.run(build_command, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"{RED}컴파일 실패!{RESET}\n명령어: {e.cmd}\n\
                표준 출력:\n{e.stdout.decode('UTF-8')}\n{RED}표준 오류:{RESET}\n{e.stderr.decode('UTF-8')}",
              file=stderr, sep='\n')
            return
        else:
            print(f"{GREEN}컴파일 성공!{RESET}")
            raw_command = compiler[lang]["run"].format(output_file=output_file)
            print(f"{YELLOW}실행:{RESET} {raw_command}\n")
            run_command=raw_command.split()
            for example in examples:
                run_test(run_command, example, write_to_file)
    else:
        print(f"{lang}:{RED} 지원되지 않는 언어입니다.{RESET}",  file=stderr)

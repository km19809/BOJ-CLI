from typing import NamedTuple
import urllib.request as req
import re
from pathlib import Path
from shutil import copyfile

def handle_argument(args:NamedTuple)->None:
    problem=args.problem
    lang=args.language
    html=req.urlopen(f"https://www.acmicpc.net/problem/{problem}").read().decode('UTF-8')
    matches=re.findall(r'<pre +class="sampledata" +id="sample-((?:input|output)-\d+)">([^<>]+)</pre>',html)
    problem_path=Path(f"./{problem}")
    problem_path.mkdir(exist_ok=True)
    for match in matches:
        with (problem_path/f"{match[0]}.txt").open('w', encoding="UTF-8") as out:
            out.write(match[1].replace("\r\n","\n"))
    with (problem_path/f"{problem}.html").open('w', encoding="UTF-8") as problem_out:
        problem_out.write(html.replace("\r\n","\n"))
    template_path=Path(f"./templates/template.{lang}")
    dest_path=problem_path/f"Main.{lang}"
    if not dest_path.exists():
        print("소스코드가 발견되지 않았습니다.")
        if template_path.exists() and template_path.is_file():
            print(f"틀({template_path})을 사용합니다.")
            copyfile(template_path,dest_path)
        else:
            print(f"틀({template_path})이 없습니다. 빈 파일을 생성합니다.")
            dest_path.open('w', encoding="UTF-8").close()
    print("다운로드 완료")
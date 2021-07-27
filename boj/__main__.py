import argparse
import get
import run
import check

parser = argparse.ArgumentParser(prog="boj",  description="백준 온라인 저지 비공식 보조도구\n예제를 다운로드하고, 작성한 코드를 실행 및 채점합니다.")
subparsers = parser.add_subparsers(help='하위 명령어')

parser_get = subparsers.add_parser("get", help="예제 입력과 출력을 다운로드합니다.")
parser_get.add_argument("problem", type=int, help="문제 번호")
parser_get.add_argument("-l","--language", default="py",
                        help="사용할 프로그래밍 언어 확장자. 틀 `templates/template.*`이 없으면 빈 파일을 생성합니다. (기본값: %(default)s)")
parser_get.set_defaults(func=get.handle_argument)

parser_run = subparsers.add_parser("run", help="작성한 프로그램을 실행합니다. 결과를 파일`result*.txt`에 작성합니다.")
parser_run.add_argument("problem", type=int, help="문제 번호")
parser_run.add_argument("-l","--language",  default="py",
                        help="사용한 프로그래밍 언어 확장자. (기본값: %(default)s)")
parser_run.add_argument("-n","--no_result",  action="store_false",dest="write_result",
                        help="사용 시, 실행만 하고 결과 파일을 저장하지 않습니다.")
parser_run.add_argument("options", default=[],
                        nargs='*', help="빌드 시 옵션을 설정합니다.")
parser_run.set_defaults(func=run.handle_argument)

parser_check = subparsers.add_parser("check", help="예제를 기반으로 채점합니다.")
parser_check.add_argument("problem", type=int, help="문제 번호")
parser_check.add_argument(
    "-v", "--verbose",  action="store_true", help="사용 시, 맞은 파일도 표시합니다.")
parser_check.set_defaults(func=check.handle_argument)

args = parser.parse_args()
args.func(args)

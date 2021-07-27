# BOJ-CLI
[백준온라인저지(BOJ)](https://www.acmicpc.net/) 예제 풀이를 위한 비공식 보조도구입니다.
## 설치 방법
```sh
git clone https://github.com/km19809/BOJ-CLI.git
```
Python 라이브러리인 `boj` 폴더와 코드 틀이 다운로드됩니다.
## 사용법
```sh
python boj -h # 도움말 보기
python boj get 1000 -l pl #1000번 문제를 저장하고 에제 파일과 틀로 Perl 소스코드를 생성
python boj run 1000 -l pl #1000번 문제에서 Perl을 실행 하고 결과를 result*.txt에 저장
python boj check 1000 -v #저장한 result*.txt와 예제 출력인 output.txt으로 채점
# or
python boj run 1000 -l pl --check #실행이 끝나는 즉시 채점
```
**기타**
* `templates` 폴더의 틀을 수정하여 원하는 템플릿을 사용할 수 있습니다.
* 입력과 출력 파일은 `input-<번호>.txt`, `output-<번호>.txt` 형태입니다.\
직접 테스트 케이스를 만들어 보세요.
* 기본적으로 지원하는 언어는 C/C++(gcc), JS, Python, Perl, Rust입니다.\
JVM(Java, Kotlin)/.NET(C#, VB)기반 언어와 Go는 테스트 되지 않았습니다.
* 추가 빌드 명령어는 `commands.json`에서 확인 및 수정할 수 있습니다.
* 추가 빌드 명령어를 사용하려면 `python boj run 1000 -l c99.c -c command.json`과 같이 사용해 보세요.
## 번들
사용하기 편하도록, 모든 Python 파일을 하나로 합친 `boj.py`를 제공합니다.
```sh
wget https://raw.githubusercontent.com/km19809/BOJ-CLI/main/bundle/boj.py

python boj.py -h
```
`commands.json`도 함께 받으면 더 좋습니다!
## 주의 사항
1. 많은 명령어가 Windows에서도 동작하나, 일부는 x64 Linux를 기본으로 작성되어 있습니다.\
x64 Linux나 WSL을 활용할 것을 권장합니다.
2. `templates` 내부 파일은 제가 작성한 것이 아닙니다.\
백준온라인 저지 [언어 도움말](https://www.acmicpc.net/help/language)을 참고하세요.
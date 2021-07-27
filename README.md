# BOJ-CLI
백준온라인저지(BOJ) 예제 풀이를 위한 부트스트래핑 보조도구입니다.
## 설치 방법
```sh
git clone https://github.com/km19809/BOJ-CLI.git
```
Python 라이브러리인 boj 폴더와 코드 틀이 다운로드됩니다.
## 사용법
```sh
boj -h
boj get 1000 -l pl #1000번 문제를 저장하고 에제 파일과 틀로 Perl 소스코드를 생성
boj run 1000 -l pl #1000번 문제에서 Perl을 실행 하고 결과를 result*.txt에 저장
boj check 1000 -v #저장한 result*.txt와 예제 출력인 output.txt으로 채점
```
**기타**
* `templates` 폴더의 틀을 수정하여 원하는 템플릿을 사용할 수 있습니다.
* 입력과 출력 파일은 `input-<번호>.txt`, `output-<번호>.txt` 형태입니다.\
직접 테스트 케이스를 만들어 보세요.
* 빌드 커맨드는 run.py에서 확인 및 수정할 수 있습니다.
## 번들
Gist에  업로드해 사용하기 편하도록, 모든 Python 파일을 하나로 합친 `boj.py`를 제공합니다.
```sh
wget https://gist.githubusercontent.com/km19809/778da27b3034692144f081c9946f0350/raw/3e3c243e9f2e764bcdd82e1c749d8c8efeb597a8/boj.py

python boj.py -h
```
## ver. Main
현재 라이브러리는 문제이름을 소스코드 이름으로 사용합니다.\
그러나 백준 온라인 저지 [언어 도움말](https://www.acmicpc.net/help/language)을 보면 파일 및 클래스의 이름이 Main인 것을 확인 할 수 있습니다.\
이에 따라 파일 이름으로 Main을 사용하며, JVM과 .NET 기반을 지원하는 버전을 제작 중에 있습니다.

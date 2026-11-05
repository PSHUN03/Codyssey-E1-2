"""자동차 로고 퀴즈 게임 실행 파일."""

import sys

from input_utils import read_number

LINE = "=" * 40

MENU_ITEMS = [
    "퀴즈 풀기",
    "퀴즈 추가",
    "퀴즈 목록",
    "점수 확인",
    "종료",
]
EXIT_CHOICE = len(MENU_ITEMS)


def show_menu():
    print()
    print(LINE)
    print("        🚗 자동차 로고 퀴즈 게임 🚗")
    print(LINE)
    for number, title in enumerate(MENU_ITEMS, start=1):
        print(f"{number}. {title}")
    print(LINE)


def run():
    while True:
        show_menu()
        choice = read_number("선택: ", 1, len(MENU_ITEMS))
        if choice == EXIT_CHOICE:
            print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
            return
        print(f"\n🚧 '{MENU_ITEMS[choice - 1]}' 기능은 준비 중입니다.")


def main():
    # 출력이 파이프/파일로 연결돼도 한글·이모지가 깨지지 않도록 UTF-8로 고정한다.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    try:
        run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️  입력이 중단되어 게임을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()

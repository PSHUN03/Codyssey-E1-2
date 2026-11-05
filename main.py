"""자동차 로고 퀴즈 게임 실행 파일."""

import sys

from quiz_game import QuizGame


def main():
    # 출력이 파이프/파일로 연결돼도 한글·이모지가 깨지지 않도록 UTF-8로 고정한다.
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n⚠️  입력이 중단되어 게임을 안전하게 종료합니다.")


if __name__ == "__main__":
    main()

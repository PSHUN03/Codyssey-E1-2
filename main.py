"""자동차 로고 퀴즈 게임 실행 파일."""

import sys

from default_quizzes import create_default_quizzes
from input_utils import read_number, read_text
from quiz import Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40

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


def play_quiz(quizzes):
    """모든 퀴즈를 순서대로 출제하고 100점 만점 점수를 반환한다."""
    if not quizzes:
        print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
        return None

    total = len(quizzes)
    print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
    correct_count = 0
    for number, quiz in enumerate(quizzes, start=1):
        print()
        print(THIN_LINE)
        quiz.display(number)
        user_answer = read_number(f"정답 입력 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
        if quiz.is_correct(user_answer):
            correct_count += 1
            print("✅ 정답입니다!")
        else:
            print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}' 입니다.")

    score = round(correct_count / total * 100)
    print()
    print(LINE)
    print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
    print(LINE)
    return score


def read_choices():
    """서로 다른 선택지 4개를 입력받아 반환한다."""
    choices = []
    while len(choices) < Quiz.CHOICE_COUNT:
        choice = read_text(f"선택지 {len(choices) + 1}: ")
        if choice in choices:
            print("⚠️  이미 입력한 선택지입니다. 다른 내용을 입력해 주세요.")
            continue
        choices.append(choice)
    return choices


def add_quiz(quizzes):
    """사용자에게 문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 추가한다."""
    print("\n📌 새로운 퀴즈를 추가합니다.")
    question = read_text("문제를 입력하세요: ")
    choices = read_choices()
    answer = read_number(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT)
    quizzes.append(Quiz(question, choices, answer))
    print(f"\n✅ 퀴즈가 추가되었습니다! (현재 {len(quizzes)}문제)")


def run():
    quizzes = create_default_quizzes()
    while True:
        show_menu()
        choice = read_number("선택: ", 1, len(MENU_ITEMS))
        if choice == EXIT_CHOICE:
            print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
            return
        if choice == 1:
            play_quiz(quizzes)
        elif choice == 2:
            add_quiz(quizzes)
        else:
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

"""게임 전체(메뉴, 진행, 퀴즈 관리, 점수)를 관리하는 QuizGame 클래스."""

from default_quizzes import create_default_quizzes
from input_utils import read_number, read_text
from quiz import Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40


class QuizGame:
    """퀴즈 목록과 최고 점수를 가지고 게임을 진행한다."""

    MENU_ITEMS = [
        "퀴즈 풀기",
        "퀴즈 추가",
        "퀴즈 목록",
        "점수 확인",
        "종료",
    ]

    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None

    # ------------------------------------------------------------------
    # 메뉴
    # ------------------------------------------------------------------
    def run(self):
        """종료를 선택할 때까지 메뉴를 반복해서 보여 준다."""
        actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_score,
        }
        exit_choice = len(self.MENU_ITEMS)
        while True:
            self.show_menu()
            choice = read_number("선택: ", 1, len(self.MENU_ITEMS))
            if choice == exit_choice:
                print("\n👋 게임을 종료합니다. 다음에 또 만나요!")
                return
            actions[choice]()

    def show_menu(self):
        print()
        print(LINE)
        print("        🚗 자동차 로고 퀴즈 게임 🚗")
        print(LINE)
        for number, title in enumerate(self.MENU_ITEMS, start=1):
            print(f"{number}. {title}")
        print(LINE)

    # ------------------------------------------------------------------
    # 게임 진행
    # ------------------------------------------------------------------
    def play_quiz(self):
        """모든 퀴즈를 출제하고 결과와 최고 점수를 갱신한다."""
        if not self.quizzes:
            self._print_empty_message()
            return

        total = len(self.quizzes)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제)")
        correct_count = 0
        for number, quiz in enumerate(self.quizzes, start=1):
            if self._ask_quiz(number, quiz):
                correct_count += 1

        score = round(correct_count / total * 100)
        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        self._update_best_score(score)
        print(LINE)

    def _ask_quiz(self, number, quiz):
        """퀴즈 한 문제를 출제하고 정답 여부를 반환한다."""
        print()
        print(THIN_LINE)
        quiz.display(number)
        user_answer = read_number(
            f"정답 입력 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT
        )
        if quiz.is_correct(user_answer):
            print("✅ 정답입니다!")
            return True
        print(f"❌ 오답입니다. 정답은 {quiz.answer}번 '{quiz.correct_choice()}' 입니다.")
        return False

    def _update_best_score(self, score):
        if self.best_score is None or score > self.best_score:
            self.best_score = score
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"🏅 현재 최고 점수는 {self.best_score}점입니다.")

    # ------------------------------------------------------------------
    # 퀴즈 관리
    # ------------------------------------------------------------------
    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 추가한다."""
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = read_text("문제를 입력하세요: ")
        choices = self._read_choices()
        answer = read_number(
            f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT
        )
        self.quizzes.append(Quiz(question, choices, answer))
        print(f"\n✅ 퀴즈가 추가되었습니다! (현재 {len(self.quizzes)}문제)")

    def _read_choices(self):
        """서로 다른 선택지 4개를 입력받아 반환한다."""
        choices = []
        while len(choices) < Quiz.CHOICE_COUNT:
            choice = read_text(f"선택지 {len(choices) + 1}: ")
            if choice in choices:
                print("⚠️  이미 입력한 선택지입니다. 다른 내용을 입력해 주세요.")
                continue
            choices.append(choice)
        return choices

    def list_quizzes(self):
        """등록된 퀴즈의 문제 목록을 출력한다."""
        if not self.quizzes:
            self._print_empty_message()
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print(THIN_LINE)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print(THIN_LINE)

    @staticmethod
    def _print_empty_message():
        print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")

    # ------------------------------------------------------------------
    # 점수
    # ------------------------------------------------------------------
    def show_score(self):
        """최고 점수를 출력한다."""
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어 보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점 (100점 만점)")

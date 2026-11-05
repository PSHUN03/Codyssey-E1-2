"""게임 전체(메뉴, 진행, 퀴즈 관리, 점수, 저장)를 관리하는 QuizGame 클래스."""

import json
import os
import random
from datetime import datetime
from pathlib import Path

from default_quizzes import create_default_quizzes
from input_utils import read_number, read_text, read_yes_no
from quiz import Quiz

LINE = "=" * 40
THIN_LINE = "-" * 40

# 실행 위치와 상관없이 항상 프로젝트 루트(이 파일이 있는 폴더)의 state.json을 사용한다.
STATE_FILE = Path(__file__).resolve().parent / "state.json"

HISTORY_DISPLAY_COUNT = 5
HISTORY_KEYS = ("played_at", "total", "correct", "score")


class QuizGame:
    """퀴즈 목록, 최고 점수, 게임 기록을 가지고 게임을 진행한다."""

    MENU_ITEMS = [
        "퀴즈 풀기",
        "퀴즈 추가",
        "퀴즈 목록",
        "점수 확인",
        "퀴즈 삭제",
        "종료",
    ]

    def __init__(self, state_path=STATE_FILE):
        self.state_path = Path(state_path)
        self.quizzes = []
        self.best_score = None
        self.history = []
        self.load_state()

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
            5: self.delete_quiz,
        }
        exit_choice = len(self.MENU_ITEMS)
        while True:
            self.show_menu()
            choice = read_number("선택: ", 1, len(self.MENU_ITEMS))
            if choice == exit_choice:
                if self.save_state():
                    print("\n💾 데이터를 저장했습니다.")
                print("👋 게임을 종료합니다. 다음에 또 만나요!")
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
        """퀴즈를 랜덤 순서로 출제하고 결과와 최고 점수를 갱신한다."""
        if not self.quizzes:
            self._print_empty_message()
            return

        available = len(self.quizzes)
        total = read_number(
            f"\n몇 문제를 풀까요? (1-{available}): ", 1, available
        )
        # 원본 목록 순서는 유지하고, 출제용으로 섞은 복사본에서 total개를 뽑는다.
        selected = random.sample(self.quizzes, total)
        print(f"\n📝 퀴즈를 시작합니다! (총 {total}문제, 랜덤 출제)")
        correct_count = 0
        for number, quiz in enumerate(selected, start=1):
            if self._ask_quiz(number, quiz):
                correct_count += 1

        score = round(correct_count / total * 100)
        print()
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct_count}문제 정답! ({score}점)")
        self._update_best_score(score)
        print(LINE)
        self.history.append({
            "played_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": total,
            "correct": correct_count,
            "score": score,
        })
        self.save_state()

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
        self.save_state()
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

    def delete_quiz(self):
        """목록에서 번호를 골라 퀴즈를 삭제하고 파일에 반영한다."""
        if not self.quizzes:
            self._print_empty_message()
            return
        self.list_quizzes()
        count = len(self.quizzes)
        number = read_number(f"삭제할 퀴즈 번호 (1-{count}, 0: 취소): ", 0, count)
        if number == 0:
            print("↩️  삭제를 취소했습니다.")
            return
        quiz = self.quizzes[number - 1]
        if not read_yes_no(f"'{quiz.question}' 퀴즈를 삭제할까요? (y/n): "):
            print("↩️  삭제를 취소했습니다.")
            return
        del self.quizzes[number - 1]
        self.save_state()
        print(f"🗑️  퀴즈를 삭제했습니다. (남은 퀴즈 {len(self.quizzes)}개)")

    @staticmethod
    def _print_empty_message():
        print("\n📭 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")

    # ------------------------------------------------------------------
    # 점수
    # ------------------------------------------------------------------
    def show_score(self):
        """최고 점수와 최근 게임 기록을 출력한다."""
        if self.best_score is None:
            print("\n📭 아직 퀴즈를 푼 기록이 없습니다. 먼저 퀴즈를 풀어 보세요!")
            return
        print(f"\n🏆 최고 점수: {self.best_score}점 (100점 만점)")
        if not self.history:
            return
        recent = self.history[-HISTORY_DISPLAY_COUNT:][::-1]
        print(f"\n📜 최근 게임 기록 (최근 {len(recent)}회 / 전체 {len(self.history)}회)")
        print(THIN_LINE)
        for record in recent:
            print(
                f"{record['played_at']} | {record['total']}문제 중 "
                f"{record['correct']}문제 정답 | {record['score']}점"
            )
        print(THIN_LINE)

    # ------------------------------------------------------------------
    # 파일 저장 / 불러오기 (state.json)
    # ------------------------------------------------------------------
    def load_state(self):
        """state.json을 불러온다. 없거나 손상되었으면 기본 데이터로 시작한다."""
        if not self.state_path.exists():
            self._reset_to_default()
            print("📂 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            self.save_state()
            return

        try:
            with open(self.state_path, encoding="utf-8") as file:
                data = json.load(file)
            quizzes, best_score, history = self._parse_state(data)
        except (OSError, ValueError) as error:
            # json.JSONDecodeError, UnicodeDecodeError도 ValueError의 하위 클래스다.
            print(f"⚠️  state.json이 손상되었거나 읽을 수 없습니다. ({error})")
            self._backup_broken_file()
            self._reset_to_default()
            print("🔧 기본 퀴즈 데이터로 복구했습니다.")
            self.save_state()
            return

        self.quizzes = quizzes
        self.best_score = best_score
        self.history = history
        score_text = "기록 없음" if best_score is None else f"{best_score}점"
        print(
            f"📂 저장된 데이터를 불러왔습니다. "
            f"(퀴즈 {len(quizzes)}개, 최고 점수 {score_text})"
        )

    def save_state(self):
        """퀴즈 목록, 최고 점수, 게임 기록을 state.json에 저장한다. 성공 여부를 반환한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "history": self.history,
        }
        # 임시 파일에 먼저 쓴 뒤 교체해서, 저장 도중 중단돼도 기존 파일이 깨지지 않게 한다.
        temp_path = self.state_path.with_name(self.state_path.name + ".tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
            os.replace(temp_path, self.state_path)
        except OSError as error:
            print(f"⚠️  데이터를 저장하지 못했습니다. ({error})")
            return False
        return True

    @staticmethod
    def _parse_state(data):
        """JSON 데이터를 검증해 (퀴즈 목록, 최고 점수, 게임 기록)으로 변환한다.

        형식이 틀리면 ValueError를 발생시킨다.
        """
        if not isinstance(data, dict):
            raise ValueError("최상위 데이터가 객체(dict) 형식이 아닙니다.")
        raw_quizzes = data.get("quizzes")
        if not isinstance(raw_quizzes, list):
            raise ValueError("quizzes 값이 목록(list)이 아닙니다.")
        quizzes = [Quiz.from_dict(item) for item in raw_quizzes]

        best_score = data.get("best_score")
        if best_score is not None and (
            isinstance(best_score, bool)
            or not isinstance(best_score, int)
            or not 0 <= best_score <= 100
        ):
            raise ValueError("best_score 값이 0~100 사이의 정수가 아닙니다.")

        # history는 보너스 기능으로 나중에 추가된 키라, 없으면 빈 기록으로 시작한다.
        history = data.get("history", [])
        if not isinstance(history, list) or not all(
            isinstance(record, dict) and all(key in record for key in HISTORY_KEYS)
            for record in history
        ):
            raise ValueError("history 값의 형식이 올바르지 않습니다.")
        return quizzes, best_score, history

    def _reset_to_default(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.history = []

    def _backup_broken_file(self):
        """손상된 파일을 state.json.bak으로 보관해 원본 내용을 잃지 않게 한다."""
        backup_path = self.state_path.with_name(self.state_path.name + ".bak")
        try:
            os.replace(self.state_path, backup_path)
            print(f"🗂️  손상된 파일은 {backup_path.name}(으)로 백업했습니다.")
        except OSError:
            pass

"""퀴즈 한 문제를 표현하는 Quiz 클래스."""


class Quiz:
    """문제(question), 선택지 4개(choices), 정답 번호(answer, 1~4)를 가진 퀴즈."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer):
        if len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        if not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답 번호는 1~{self.CHOICE_COUNT} 사이여야 합니다.")
        self.question = question
        self.choices = list(choices)
        self.answer = answer

    def display(self, number=None):
        """문제와 선택지를 화면에 출력한다."""
        title = f"[문제 {number}]" if number is not None else "[문제]"
        print(title)
        print(self.question)
        print()
        for index, choice in enumerate(self.choices, start=1):
            print(f"  {index}. {choice}")
        print()

    def is_correct(self, user_answer):
        """사용자가 고른 번호가 정답인지 확인한다."""
        return user_answer == self.answer

    def correct_choice(self):
        """정답 선택지의 내용을 반환한다."""
        return self.choices[self.answer - 1]

    def to_dict(self):
        """state.json에 저장할 수 있는 딕셔너리로 변환한다."""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        """state.json에서 읽은 딕셔너리로 Quiz를 만든다. 형식이 틀리면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 항목이 객체(dict) 형식이 아닙니다.")
        question = data.get("question")
        choices = data.get("choices")
        answer = data.get("answer")
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question 값이 비어 있거나 문자열이 아닙니다.")
        if not isinstance(choices, list) or not all(
            isinstance(choice, str) and choice.strip() for choice in choices
        ):
            raise ValueError("choices 값이 문자열 목록이 아닙니다.")
        # bool은 int의 하위 타입이라 True/False가 1/0으로 통과하지 않도록 따로 막는다.
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise ValueError("answer 값이 정수가 아닙니다.")
        return cls(question, choices, answer)

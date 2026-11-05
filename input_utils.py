"""콘솔 입력을 안전하게 받기 위한 보조 함수 모음.

모든 입력은 앞뒤 공백을 제거한 뒤 처리하며,
잘못된 입력이 들어오면 안내 메시지를 출력하고 다시 입력받는다.
"""


def read_text(prompt):
    """빈 값이 아닌 문자열을 입력받아 반환한다."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("⚠️  빈 입력입니다. 내용을 입력해 주세요.")


def read_number(prompt, min_value, max_value):
    """min_value 이상 max_value 이하의 정수를 입력받아 반환한다."""
    guide = f"{min_value}-{max_value} 사이의 숫자를 입력하세요."
    while True:
        raw = input(prompt).strip()
        if not raw:
            print(f"⚠️  빈 입력입니다. {guide}")
            continue
        try:
            number = int(raw)
        except ValueError:
            print(f"⚠️  잘못된 입력입니다. {guide}")
            continue
        if not min_value <= number <= max_value:
            print(f"⚠️  범위를 벗어난 숫자입니다. {guide}")
            continue
        return number

"""Вспомогательные функции безопасного пользовательского ввода."""


def input_int(prompt: str, minimum: int | None = None) -> int:
    """Получить целое число и повторить запрос при ошибке."""
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное целое число")


def input_float(prompt: str, minimum: float | None = None) -> float:
    """Получить вещественное число и повторить запрос при ошибке."""
    while True:
        try:
            value = float(input(prompt))
            if minimum is not None and value < minimum:
                raise ValueError
            return value
        except ValueError:
            print("Введите корректное число")

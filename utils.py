"""Вспомогательные функции консольного интерфейса."""


def input_int(prompt: str, minimum: int = 0) -> int:
    """Получить целое число не меньше заданного минимума."""
    value = int(input(prompt))
    if value < minimum:
        raise ValueError(f"Значение должно быть не меньше {minimum}")
    return value

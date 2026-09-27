"""Вспомогательные функции ввода и работы с датой."""

from datetime import datetime


DATE_FORMAT = "%Y-%m-%d %H:%M"


def parse_datetime(value: str) -> datetime:
    """Преобразовать строку в дату и время."""
    try:
        return datetime.strptime(value.strip(), DATE_FORMAT)
    except ValueError as error:
        raise ValueError("Используйте формат ГГГГ-ММ-ДД ЧЧ:ММ") from error


def input_int(prompt: str, minimum: int = 0) -> int:
    """Получить целое число не меньше заданного минимума."""
    value = int(input(prompt))
    if value < minimum:
        raise ValueError(f"Значение должно быть не меньше {minimum}")
    return value

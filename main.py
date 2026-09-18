"""Начальный сценарий проекта «Коллекция скинов Counter-Strike»."""

from decimal import Decimal


SKIN_NAME = "AK-47 | Redline"
SKIN_PRICE = Decimal("2350.00")
USER_BALANCE = Decimal("5000.00")
MIN_WEAR = 0.10
MAX_WEAR = 0.70
IS_AVAILABLE = True


def get_skin_condition(wear: float) -> str:
    """Определить состояние скина по значению износа."""
    if wear < 0 or wear > 1:
        return "Некорректное значение износа"
    if wear < 0.07:
        return "Прямо с завода"
    if wear < 0.15:
        return "Немного поношенное"
    if wear < 0.38:
        return "После полевых испытаний"
    if wear < 0.45:
        return "Поношенное"
    return "Закалённое в боях"


def is_wear_allowed(wear: float, min_wear: float, max_wear: float) -> bool:
    """Проверить, входит ли износ экземпляра в диапазон выбранного скина."""
    return min_wear <= wear <= max_wear


def calculate_balance_after_purchase(
    balance: Decimal,
    price: Decimal,
) -> Decimal:
    """Рассчитать остаток средств после покупки скина."""
    return balance - price


def get_purchase_status(
    is_available: bool,
    wear_allowed: bool,
    balance_after_purchase: Decimal,
) -> str:
    """Вернуть результат проверки возможности покупки."""
    if not is_available:
        return "Скин сейчас недоступен"
    if not wear_allowed:
        return "Износ не соответствует диапазону выбранного скина"
    if balance_after_purchase < 0:
        return "Недостаточно средств для покупки"
    return "Скин можно добавить в коллекцию"


def main() -> None:
    """Запустить проверку покупки одного экземпляра скина."""
    print("Система учёта коллекции скинов Counter-Strike")
    print(f"Скин: {SKIN_NAME}")
    print(f"Цена: {SKIN_PRICE:.2f} руб.")
    print(f"Баланс: {USER_BALANCE:.2f} руб.")

    wear = float(input("Введите износ экземпляра от 0 до 1: "))
    condition = get_skin_condition(wear)
    wear_allowed = is_wear_allowed(wear, MIN_WEAR, MAX_WEAR)
    balance_after_purchase = calculate_balance_after_purchase(
        USER_BALANCE,
        SKIN_PRICE,
    )
    status = get_purchase_status(
        IS_AVAILABLE,
        wear_allowed,
        balance_after_purchase,
    )

    print(f"Состояние: {condition}")
    print(f"Результат: {status}")
    if status == "Скин можно добавить в коллекцию":
        print(f"Остаток после покупки: {balance_after_purchase:.2f} руб.")


if __name__ == "__main__":
    main()

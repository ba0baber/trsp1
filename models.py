"""Объектная модель системы учёта коллекции скинов."""

from dataclasses import dataclass
from typing import Any


def get_skin_condition(wear: float) -> str:
    """Определить состояние скина по значению износа."""
    if not 0 <= wear <= 1:
        raise ValueError("Износ должен находиться в диапазоне от 0 до 1")
    if wear < 0.07:
        return "Прямо с завода"
    if wear < 0.15:
        return "Немного поношенное"
    if wear < 0.38:
        return "После полевых испытаний"
    if wear < 0.45:
        return "Поношенное"
    return "Закалённое в боях"


@dataclass
class Skin:
    """Скин из каталога."""

    id: int
    name: str
    weapon: str
    price: float
    wear: float
    rarity: str
    is_available: bool = True

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.weapon.strip():
            raise ValueError("Название и оружие не могут быть пустыми")
        if self.price < 0:
            raise ValueError("Цена не может быть отрицательной")
        get_skin_condition(self.wear)

    @property
    def condition(self) -> str:
        """Вернуть состояние, вычисленное по износу."""
        return get_skin_condition(self.wear)

    def mark_sold(self) -> None:
        """Пометить скин как находящийся в коллекции."""
        if not self.is_available:
            raise ValueError("Скин сейчас недоступен")
        self.is_available = False

    def mark_available(self) -> None:
        """Вернуть скин в доступный каталог."""
        self.is_available = True

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать объект в JSON-совместимый словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "weapon": self.weapon,
            "price": self.price,
            "wear": self.wear,
            "condition": self.condition,
            "rarity": self.rarity,
            "is_available": self.is_available,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Skin":
        """Создать объект из словаря, загруженного из JSON."""
        try:
            return cls(
                id=int(data["id"]), name=str(data["name"]),
                weapon=str(data["weapon"]), price=float(data["price"]),
                wear=float(data["wear"]), rarity=str(data["rarity"]),
                is_available=bool(data["is_available"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Некорректные данные скина") from error

    def __str__(self) -> str:
        availability = "доступен" if self.is_available else "в коллекции"
        return (
            f"{self.id}. {self.weapon} | {self.name}; {self.condition}; "
            f"{self.price:.2f} руб.; {availability}"
        )


class User:
    """Пользователь с защищённым от прямого изменения балансом."""

    def __init__(self, name: str, balance: float) -> None:
        if not name.strip():
            raise ValueError("Имя владельца не может быть пустым")
        if balance < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self.name = name.strip()
        self._balance = round(balance, 2)

    @property
    def balance(self) -> float:
        """Вернуть текущий баланс пользователя."""
        return self._balance

    def pay(self, amount: float) -> None:
        """Списать стоимость покупки при достаточном балансе."""
        if amount > self._balance:
            raise ValueError("Недостаточно средств для покупки")
        self._balance = round(self._balance - amount, 2)

    def __str__(self) -> str:
        return f"{self.name}, баланс: {self.balance:.2f} руб."


@dataclass
class CollectionItem:
    """Запись о покупке скина пользователем."""

    id: int
    owner: str
    skin_id: int
    purchase_price: float

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать запись в JSON-совместимый словарь."""
        return {
            "id": self.id, "owner": self.owner,
            "skin_id": self.skin_id, "purchase_price": self.purchase_price,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CollectionItem":
        """Создать запись из словаря, загруженного из JSON."""
        try:
            return cls(
                id=int(data["id"]), owner=str(data["owner"]),
                skin_id=int(data["skin_id"]),
                purchase_price=float(data["purchase_price"]),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Некорректные данные записи коллекции") from error

    def __str__(self) -> str:
        return (
            f"Запись {self.id}: владелец {self.owner}, скин {self.skin_id}, "
            f"цена покупки {self.purchase_price:.2f} руб."
        )

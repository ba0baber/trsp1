"""Сущность пользователя."""

from typing import Any


class User:
    """Пользователь, который организует мероприятия."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        if not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        self.id = user_id
        self.name = name.strip()
        self.email = email

    @property
    def email(self) -> str:
        """Вернуть адрес электронной почты."""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Некорректный адрес электронной почты")
        self._email = value.strip().lower()

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать пользователя в JSON-словарь."""
        return {"id": self.id, "name": self.name, "email": self.email}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        """Создать пользователя из JSON-словаря."""
        try:
            return cls(int(data["id"]), str(data["name"]), str(data["email"]))
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("Некорректные данные пользователя") from error

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"

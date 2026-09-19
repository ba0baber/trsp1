"""Чтение и запись данных проекта в формате JSON."""

import json
from pathlib import Path
from typing import Any


class StorageError(Exception):
    """Ошибка чтения или записи данных проекта."""


def load_json(path: Path) -> list[dict[str, Any]]:
    """Загрузить список из JSON; для отсутствующего файла вернуть []."""
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise StorageError(f"Не удалось загрузить данные из {path}") from error
    if not isinstance(data, list):
        raise StorageError(f"В файле {path} должен находиться список")
    return data


def save_json(path: Path, data: list[dict[str, Any]]) -> None:
    """Сохранить список в JSON."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise StorageError(f"Не удалось сохранить данные в {path}") from error

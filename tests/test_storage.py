import json

import pytest

from storage import StorageError, load_json, save_json


def test_save_and_load_json(tmp_path):
    path = tmp_path / "data.json"
    data = [{"id": 1, "name": "Аудитория 301"}]
    save_json(path, data)
    assert load_json(path) == data


def test_load_missing_file_returns_empty_list(tmp_path):
    assert load_json(tmp_path / "missing.json") == []


def test_load_invalid_json_raises_storage_error(tmp_path):
    path = tmp_path / "broken.json"
    path.write_text("{broken", encoding="utf-8")
    with pytest.raises(StorageError):
        load_json(path)


def test_load_rejects_non_list_json(tmp_path):
    path = tmp_path / "object.json"
    path.write_text(json.dumps({"id": 1}), encoding="utf-8")
    with pytest.raises(StorageError, match="список"):
        load_json(path)

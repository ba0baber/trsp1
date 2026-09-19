import json

import pytest

from collection import Collection
from models import CollectionItem, Skin
from storage import (
    StorageError,
    load_collection,
    load_json,
    load_skins,
    save_collection,
    save_json,
    save_skins,
)


def test_save_and_load_json(tmp_path):
    path = tmp_path / "data.json"
    data = [{"id": 1, "name": "Redline"}]
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


def test_skin_objects_round_trip_json(tmp_path):
    path = tmp_path / "skins.json"
    save_skins(path, [Skin(1, "Redline", "AK-47", 2350, 0.25, "Тайное")])
    loaded = load_skins(path)
    assert isinstance(loaded[0], Skin)
    assert loaded[0].condition == "После полевых испытаний"


def test_collection_object_round_trip_json(tmp_path):
    path = tmp_path / "collection.json"
    source = Collection([CollectionItem(1, "Варвара", 1, 2350)])
    save_collection(path, source)
    loaded = load_collection(path)
    assert isinstance(loaded, Collection)
    assert isinstance(loaded.items[0], CollectionItem)
    assert loaded.total_value() == 2350

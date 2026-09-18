import pytest

from collection import (
    add_to_collection,
    calculate_collection_value,
    find_owner_items,
    remove_from_collection,
)


def sample_skins():
    return [
        {
            "id": 1,
            "name": "Redline",
            "weapon": "AK-47",
            "price": 2350.0,
            "wear": 0.25,
            "condition": "После полевых испытаний",
            "rarity": "Засекреченное",
            "is_available": True,
        }
    ]


def test_add_to_collection_marks_skin_unavailable():
    skins = sample_skins()
    collection = []
    item = add_to_collection(collection, skins, "Варвара", 1, 5000)
    assert item["skin_id"] == 1
    assert skins[0]["is_available"] is False


def test_add_to_collection_rejects_insufficient_balance():
    with pytest.raises(ValueError, match="Недостаточно"):
        add_to_collection([], sample_skins(), "Варвара", 1, 100)


def test_duplicate_purchase_is_forbidden():
    skins = sample_skins()
    collection = []
    add_to_collection(collection, skins, "Варвара", 1, 5000)
    with pytest.raises(ValueError, match="недоступен"):
        add_to_collection(collection, skins, "Варвара", 1, 5000)


def test_remove_from_collection_restores_availability():
    skins = sample_skins()
    collection = []
    item = add_to_collection(collection, skins, "Варвара", 1, 5000)
    remove_from_collection(collection, skins, int(item["id"]))
    assert collection == []
    assert skins[0]["is_available"] is True


def test_calculate_collection_value():
    collection = [
        {"id": 1, "owner": "Варвара", "skin_id": 1, "purchase_price": 100},
        {"id": 2, "owner": "Варвара", "skin_id": 2, "purchase_price": 250},
    ]
    assert calculate_collection_value(collection) == 350


def test_find_owner_items_is_case_insensitive():
    collection = [
        {"id": 1, "owner": "Варвара", "skin_id": 1, "purchase_price": 100},
        {"id": 2, "owner": "Иван", "skin_id": 2, "purchase_price": 250},
    ]
    assert len(find_owner_items(collection, "варвара")) == 1

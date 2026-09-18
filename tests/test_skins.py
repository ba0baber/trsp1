import pytest

from skins import (
    add_skin,
    filter_skins_by_price,
    find_skins,
    get_skin_condition,
    iter_skins_by_rarity,
    sort_skins_by_price,
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
        },
        {
            "id": 2,
            "name": "Asiimov",
            "weapon": "AWP",
            "price": 9200.0,
            "wear": 0.41,
            "condition": "Поношенное",
            "rarity": "Тайное",
            "is_available": False,
        },
    ]


def test_get_skin_condition():
    assert get_skin_condition(0.25) == "После полевых испытаний"


def test_get_skin_condition_rejects_invalid_wear():
    with pytest.raises(ValueError):
        get_skin_condition(1.2)


def test_add_skin_assigns_next_id():
    skins = sample_skins()
    skin = add_skin(skins, "Neo-Noir", "USP-S", 3500, 0.1, "Тайное")
    assert skin["id"] == 3
    assert len(skins) == 3


def test_find_skins_is_case_insensitive():
    assert find_skins(sample_skins(), "ak-47")[0]["name"] == "Redline"


def test_filter_skins_by_price_returns_available_only():
    result = filter_skins_by_price(sample_skins(), 10000)
    assert [skin["id"] for skin in result] == [1]


def test_sort_skins_by_price():
    result = sort_skins_by_price(sample_skins())
    assert [skin["id"] for skin in result] == [1, 2]


def test_generator_filters_by_rarity():
    result = list(iter_skins_by_rarity(sample_skins(), "тайное"))
    assert [skin["id"] for skin in result] == [2]

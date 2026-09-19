import pytest

from models import Skin, get_skin_condition
from skins import (
    add_skin, filter_skins_by_price, find_skins,
    iter_skins_by_rarity, sort_skins_by_price,
)


def sample_skins():
    return [
        Skin(1, "Redline", "AK-47", 2350, 0.25, "Засекреченное"),
        Skin(2, "Asiimov", "AWP", 9200, 0.41, "Тайное", False),
    ]


def test_skin_has_condition_and_string_representation():
    skin = sample_skins()[0]
    assert skin.condition == "После полевых испытаний"
    assert "AK-47 | Redline" in str(skin)


def test_get_skin_condition_rejects_invalid_wear():
    with pytest.raises(ValueError):
        get_skin_condition(1.2)


def test_add_skin_assigns_next_id():
    skins = sample_skins()
    skin = add_skin(skins, "Neo-Noir", "USP-S", 3500, 0.1, "Тайное")
    assert skin.id == 3
    assert len(skins) == 3


def test_find_skins_is_case_insensitive():
    assert find_skins(sample_skins(), "ak-47")[0].name == "Redline"


def test_filter_skins_by_price_returns_available_only():
    result = filter_skins_by_price(sample_skins(), 10000)
    assert [skin.id for skin in result] == [1]


def test_sort_skins_by_price():
    assert [skin.id for skin in sort_skins_by_price(sample_skins())] == [1, 2]


def test_generator_filters_by_rarity():
    result = list(iter_skins_by_rarity(sample_skins(), "тайное"))
    assert [skin.id for skin in result] == [2]

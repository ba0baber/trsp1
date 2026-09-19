import pytest

from collection import Collection
from models import CollectionItem, Skin, User


def sample_skins():
    return [Skin(1, "Redline", "AK-47", 2350, 0.25, "Засекреченное")]


def test_purchase_connects_user_skin_and_collection():
    skins = sample_skins()
    user = User("Варвара", 5000)
    collection = Collection()
    item = collection.purchase(skins, user, 1)
    assert item.skin_id == skins[0].id
    assert item.owner == user.name
    assert user.balance == 2650
    assert skins[0].is_available is False


def test_purchase_rejects_insufficient_balance():
    with pytest.raises(ValueError, match="Недостаточно"):
        Collection().purchase(sample_skins(), User("Варвара", 100), 1)


def test_duplicate_purchase_is_forbidden():
    skins = sample_skins()
    collection = Collection()
    collection.purchase(skins, User("Варвара", 5000), 1)
    with pytest.raises(ValueError, match="недоступен"):
        collection.purchase(skins, User("Варвара", 5000), 1)


def test_remove_restores_availability():
    skins = sample_skins()
    collection = Collection()
    item = collection.purchase(skins, User("Варвара", 5000), 1)
    collection.remove(skins, item.id)
    assert collection.items == []
    assert skins[0].is_available is True


def test_total_value_and_string_representation():
    collection = Collection([
        CollectionItem(1, "Варвара", 1, 100),
        CollectionItem(2, "Варвара", 2, 250),
    ])
    assert collection.total_value() == 350
    assert "Стоимость коллекции: 350.00" in str(collection)


def test_find_by_owner_is_case_insensitive():
    collection = Collection([
        CollectionItem(1, "Варвара", 1, 100),
        CollectionItem(2, "Иван", 2, 250),
    ])
    assert len(collection.find_by_owner("варвара")) == 1


def test_user_validates_name_and_protects_balance():
    with pytest.raises(ValueError, match="Имя"):
        User(" ", 100)
    assert User("Варвара", 100).balance == 100

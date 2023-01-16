from pytest import fixture
from src.pymongo_db import MongoDb


@fixture(scope="module")
def test_db():
    """
    Test fixture yielding MongoDb object with 'test_db' database and 'test_collection' collection
    :return: MongoDb object
    """
    return_database = MongoDb("puzzling_orangutan", "main")
    yield return_database
    return_database.mongo["puzzling_orangutan"].drop_collection("main")

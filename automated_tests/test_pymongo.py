from pytest import mark, raises
from src.exceptions import *


@mark.pymongo
def test__create_user_when_username_provided(test_db):
    """
    Verifies: OBJ-19
    Verifies: OBJ-23
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {"username": "new_user"}
    expected_data = {"username": "new_user", "services": [], "object_type": "user"}
    actual_data = test_db.create_user(test_data["username"])
    assert actual_data != -1, "Inserted object return id is -1."
    actual_data = test_db.find(test_data)
    assert actual_data == expected_data, f"Actual data is different that expected. Actual: {actual_data}, Expected: 1"


@mark.pymongo
def test__create_user_when_username_exists(test_db):
    """
    Verifies: OBJ-20
    Verifies: OBJ-23
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {"username": "new_user"}
    with raises(UsernameAlreadyExists):
        test_db.create_user(test_data["username"])
    actual_data = len(test_db.find_all(test_data))
    assert actual_data == 1, f"Size of returned query does not equal 1. Actual: {actual_data}, Expected: 1"


@mark.pymongo
def test__create_service_when_service_name_provided(test_db):
    """
    Verifies: OBJ-21
    Verifies: OBJ-23
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {"service": "new_service"}
    expected_data = {"service": "new_service", "status": "not_finished", "object_type": "service"}
    actual_data = test_db.create_service(test_data["service"])
    assert actual_data != -1, "Inserted object return id is -1."
    actual_data = test_db.find(test_data)
    assert actual_data == expected_data, f"Actual data is different that expected. " \
                                         f"Actual: {actual_data}, Expected: {expected_data}"


@mark.pymongo
def test__create_service_when_service_exists(test_db):
    """
    Verifies: OBJ-22
    Verifies: OBJ-23
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {"service": "new_service"}
    with raises(ServiceAlreadyExists):
        test_db.create_service(test_data["service"])
    actual_data = len(test_db.find_all(test_data))
    assert actual_data == 1, f"Size of returned query does not equal 1. Actual: {actual_data}, Expected: 1"


@mark.pymongo
def test__subscribe_service_with_proper_values(test_db):
    """
    Verifies: OBJ-24
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {"username": "new_user", "service": "new_service"}
    test_db.subscribe_service(test_data["username"], test_data["service"])
    actual_data = test_db.find({"username": test_data["username"]})
    assert "new_service" in actual_data["services"], f"User was not subscribed to service. Actual: {actual_data}"


@mark.pymongo
def test__subscribe_service_with_wrong_username_provided(test_db):
    """
    Verifies: OBJ-25
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {"username": "not_existing", "service": "new_service"}
    with raises(UsernameDoesntExists):
        test_db.subscribe_service(test_data["username"], test_data["service"])


@mark.pymongo
def test__subscribe_service_with_wrong_service_name_provided(test_db):
    """
    Verifies: OBJ-26
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {"username": "new_user", "service": "not_existing"}
    with raises(ServiceDoesntExists):
        test_db.subscribe_service(test_data["username"], test_data["service"])


@mark.pymongo
def test__subscribe_service_with_already_active_subscription(test_db):
    """
    Verifies: OBJ-27
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {"username": "new_user", "service": "new_service"}
    with raises(ServiceIsAlreadySubscribed):
        test_db.subscribe_service(test_data["username"], test_data["service"])

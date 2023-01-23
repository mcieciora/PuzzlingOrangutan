from pytest import fixture
from requests import get


@fixture(scope="module")
def endpoints_fixture():
    """
    Test fixture clearing database collection at the end of test execution
    :return: MongoDb object
    """
    yield
    with open('test_key', 'r') as secret_key_file:
        secret_key = secret_key_file.read()
    get(f"http://localhost:8007/clear/{secret_key}", timeout=5)

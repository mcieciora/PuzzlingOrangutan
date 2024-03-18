from pytest import fixture


@fixture
def expected_status_code():
    yield 200

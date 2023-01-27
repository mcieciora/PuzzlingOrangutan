from requests import get
from pytest import mark

class TestEndpointsClass:
    """
    TestEndpointsClass contains main, create_user, get_subscriptions, get_service, create_service, subscribe
    endpoints tests
    """
    @staticmethod
    def teardown_class():
        """
        Teardown function clearing database collection after testing.
        :return: None
        """
        with open('automated_tests/test_key', 'r', encoding='utf-8') as secret_key_file:
            secret_key = secret_key_file.read()
        get(f"http://localhost:8007/clear/{secret_key}", timeout=5)

    @mark.endpoints
    def test__check_index_endpoint_status(self):
        """
        TestCase: OBJ-14
        Verifies: OBJ-4
        :return: None
        """
        expected_data = {"status": 200, "message": "I'm ok, you?"}
        actual_data = get("http://localhost:8007/", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__create_user_when_username_provided_by_endpoint(self):
        """
        TestCase: OBJ-10
        Verifies: OBJ-2
        :return: None
        """
        expected_data = {"status": 200, "message": "User new_user created successfully."}
        actual_data = get("http://localhost:8007/create_user/new_user", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__cannot_create_user_when_the_same_username_provided_by_endpoint(self):
        """
        TestCase: OBJ-11
        Verifies: OBJ-2
        :return: None
        """
        expected_data = {"status": 400, "message": "Cannot create user cause username already exists"}
        actual_data = get("http://localhost:8007/create_user/new_user", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__get_list_of_all_users_with_subscriptions_by_endpoint(self):
        """
        TestCase: OBJ-29
        Verifies: OBJ-28
        :return: None
        """
        expected_data = {"new_user": []}
        actual_data = get("http://localhost:8007/get_subscriptions", timeout=5)
        assert actual_data.json() == expected_data, f"Endpoint return is different than expected. " \
                                                    f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__create_service_when_service_name_provided_by_endpoint(self):
        """
        TestCase: OBJ-13
        Verifies: OBJ-3
        :return: None
        """
        expected_data = {"status": 200, "message": "Service new_service created successfully"}
        actual_data = get("http://localhost:8007/create_service/new_service", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__create_service_when_username_provided_by_endpoint(self):
        """
        TestCase: OBJ-12
        Verifies: OBJ-2
        :return: None
        """
        expected_data = {"status": 400, "message": "Cannot create service cause it already exists"}
        actual_data = get("http://localhost:8007/create_service/new_service", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__subscribe_to_service_with_proper_values_by_endpoint(self):
        """
        TestCase: OBJ-15
        Verifies: OBJ-5
        :return: None
        """
        expected_data = {"status": 200, "message": "User new_user subscribed to new_service."}
        actual_data = get("http://localhost:8007/subscribe/new_user/new_service", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__subscribe_service_with_wrong_username_provided_by_endpoint(self):
        """
        TestCase: OBJ-16
        Verifies: OBJ-5
        :return: None
        """
        expected_data = {"status": 400, "message": "Cannot subscribe service cause username does not exist."}
        actual_data = get("http://localhost:8007/subscribe/not_existing/new_service", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__subscribe_service_with_wrong_service_name_provided_by_endpoint(self):
        """
        TestCase: OBJ-17
        Verifies: OBJ-5
        :return: None
        """
        expected_data = {"status": 400, "message": "Cannot subscribe service cause service does not exist."}
        actual_data = get("http://localhost:8007/subscribe/new_user/not_existing", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__subscribe_service_with_already_active_subscription_by_endpoint(self):
        """
        TestCase: OBJ-18
        Verifies: OBJ-5
        :return: None
        """
        expected_data = {"status": 400, "message": "Cannot subscribe service cause it is already subscribed."}
        actual_data = get("http://localhost:8007/subscribe/new_user/new_service", timeout=5)
        assert actual_data.json()["data"] == expected_data, f"Endpoint return is different than expected. " \
                                                            f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__get_list_of_all_users_with_active_subscriptions_by_endpoint(self):
        """
        TestCase: OBJ-29
        Verifies: OBJ-28
        :return: None
        """
        expected_data = {"new_user": ["new_service"]}
        actual_data = get("http://localhost:8007/get_subscriptions", timeout=5)
        assert actual_data.json() == expected_data, f"Endpoint return is different than expected. " \
                                                    f"Actual: {actual_data}, Expected: {expected_data}"

    @mark.endpoints
    def test__get_list_of_all_services_by_endpoint(self):
        """
        TestCase: OBJ-14
        Verifies: OBJ-4
        :return: None
        """
        expected_data = {"new_service": "not_finished"}
        actual_data = get("http://localhost:8007/get_services", timeout=5)
        assert actual_data.json() == expected_data, f"Endpoint return is different than expected. " \
                                                    f"Actual: {actual_data}, Expected: {expected_data}"

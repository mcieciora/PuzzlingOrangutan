from bottle import route, run
from pymongo_db import MongoDb
from exceptions import UsernameDoesntExists, UsernameAlreadyExists, ServiceDoesntExists, ServiceAlreadyExists, \
    ServiceIsAlreadySubscribed


@route("/")
def index():
    """
    Main endpoint.
    :return: Status message 200 if app and database is running.
    """
    return_value = {"status": 200, "message": "I'm ok, you?"}
    return dict(data=return_value)


@route("/create_user/<username>")
def create_user(username):
    """
    Create user endpoint.
    :param username: user to create string value
    :return: Status 200 if user was created else status 400.
    """
    try:
        mongo_client.create_user(username)
        return_value = {"status": 200, "message": f"User {username} created successfully."}
    except UsernameAlreadyExists:
        return_value = {"status": 400, "message": "Cannot create user cause username already exists"}
    return dict(data=return_value)


@route("/create_service/<service_name>")
def create_service(service_name):
    """
    Create service endpoint.
    :param service_name: service to create string value
    :return: Status 200 if service was created else status 400.
    """
    try:
        mongo_client.create_service(service_name)
        return_value = {"status": 200, "message": f"Service {service_name} created successfully"}
    except ServiceAlreadyExists:
        return_value = {"status": 400, "message": "Cannot create service cause it already exists"}
    return dict(data=return_value)


@route("/subscribe/<username>/<service>")
def subscribe(username, service):
    """
    Subscribe endpoint.
    :param username: user string value
    :param service: service to subscribe string value
    :return: Status 200 if subscription was successful else status 400 with various return messages.
    """
    try:
        mongo_client.subscribe_service(username, service)
        return_value = {"status": 200, "message": f"User {username} subscribed to {service}."}
    except UsernameDoesntExists:
        return_value = {"status": 400, "message": "Cannot subscribe service cause username does not exist."}
    except ServiceDoesntExists:
        return_value = {"status": 400, "message": "Cannot subscribe service cause service does not exist."}
    except ServiceIsAlreadySubscribed:
        return_value = {"status": 400, "message": "Cannot subscribe service cause it is already subscribed."}
    return dict(data=return_value)


@route("/get_subscriptions")
def get_subscriptions():
    """
    Get subscriptions endpoint.
    :return: List of all subscriptions in String<user_name>: List<service_name> convention.
    """
    return_dict = {}
    for element in mongo_client.find_all({"object_type": "user"}):
        return_dict[element["username"]] = element["services"]
    return return_dict


@route("/get_services")
def get_services():
    """
    Get services endpoint.
    :return: List of all services in String<service_name>: String<service_status>
    """
    return_dict = {}
    for service in mongo_client.find_all({"object_type": "service"}):
        return_dict[service["service"]] = service["status"]
    return return_dict


@route("/clear/<secret_key>")
def clear(secret_key):
    """
    Clear endpoint.
    :param secret_key: Secret key that is compared to value stored in secret_key file
    :return:
    """
    with open('secret_key', 'r', encoding='utf-8') as secret_key_file:
        if secret_key_file.read() == secret_key:
            mongo_client.clear()
            return_value = {"status": 200, "message": "Collection has been dropped."}
        else:
            return_value = {"status": 400, "message": "Wrong secret key value."}
    return dict(data=return_value)


if __name__ == "__main__":
    mongo_client = MongoDb("puzzling_orangutan", "main")
    run(host="0.0.0.0", port=8007)

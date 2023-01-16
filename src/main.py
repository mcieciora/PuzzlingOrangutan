from bottle import route, run
from pymongo_db import MongoDb
import src.exceptions


@route("/")
def index():
    return_value = {"status": 200, "message": "I'm ok, you?"}
    return dict(data=return_value)


@route("/create_user/<username>")
def create_user(username):
    try:
        mongo_client.create_user(username)
        return_value = {"status": 200, "message": f"User {username} created successfully."}
    except src.exceptions.UsernameAlreadyExists:
        return_value = {"status": 400, "message": "Cannot create user cause username already exists"}
    return dict(data=return_value)


@route("/create_service/<service_name>")
def create_service(service_name):
    try:
        mongo_client.create_service(service_name)
        return_value = {"status": 200, "message": f"Service {service_name} created successfully"}
    except src.exceptions.ServiceAlreadyExists:
        return_value = {"status": 400, "message": "Cannot create service cause it already exists"}
    return dict(data=return_value)


@route("/subscribe/<username>/<service>")
def subscribe(username, service):
    try:
        mongo_client.subscribe_service(username, service)
        return_value = {"status": 200, "message": f"User {username} subscribed to {service}."}
    except src.exceptions.UsernameDoesntExists:
        return_value = {"status": 400, "message": "Cannot subscribe service cause username does not exist."}
    except src.exceptions.ServiceDoesntExists:
        return_value = {"status": 400, "message": "Cannot subscribe service cause service does not exist."}
    except src.exceptions.ServiceIsAlreadySubscribed:
        return_value = {"status": 400, "message": "Cannot subscribe service cause it is already subscribed."}
    return dict(data=return_value)


@route("/get_subscriptions")
def get_subscriptions():
    return_dict = {}
    for element in mongo_client.find_all({"object_type": "user"}):
        return_dict[element["username"]] = element["services"]
    return return_dict


@route("/get_services")
def get_services():
    return_dict = {}
    for service in mongo_client.find_all({"object_type": "service"}):
        return_dict[service["service"]] = service["status"]
    return return_dict


if __name__ == "__main__":
    mongo_client = MongoDb("puzzling_orangutan", "main")
    run(host="0.0.0.0", port=8007)

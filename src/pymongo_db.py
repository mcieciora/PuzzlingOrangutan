from pymongo import MongoClient
from exceptions import UsernameAlreadyExists, ServiceAlreadyExists, UsernameDoesntExists, \
    ServiceIsAlreadySubscribed, ServiceDoesntExists


class MongoDb:
    """
    MongoDB is a class to operate on database with usage of pymongo library.
    """
    def __init__(self, db_name, collection_name):
        self.mongo = MongoClient(host="mongodb", port=27017)
        self.collection = self.mongo[db_name][collection_name]

    def find(self, query):
        """
        Find function searches database with given query
        :param query: dict type object that consists of searched value
        :return: one object meeting criteria
        """
        query_search = self.collection.find_one(query, projection={"_id": False})
        return query_search

    def find_all(self, query):
        """
        Find function searches database with given query
        :param query: dict type object that consists of searched value
        :return: list of found database objects
        """
        query_search = self.collection.find(query, projection={"_id": False})
        return list(query_search)

    def create_user(self, username):
        """
        Create new user if it does not already exist, this function raises UsernameAlreadyExists exception
        :param username: username string value
        :return: inserted_id value
        """
        query_search = self.find({"username": username})
        if query_search:
            raise UsernameAlreadyExists
        username_object = {"username": username, "services": [], "object_type": "user"}
        return self.collection.insert_one(username_object).inserted_id

    def create_service(self, service_name):
        """
        Create new service if it does not already exist, this function raises ServiceAlreadyExists exception
        :param service_name: service name string value
        :return: inserted_id value
        """
        query_search = self.find({"service": service_name})
        if query_search:
            raise ServiceAlreadyExists
        username_object = {"service": service_name, "status": "not_finished", "object_type": "service"}
        return self.collection.insert_one(username_object).inserted_id

    def subscribe_service(self, username, service_name):
        """
        Subscribe function checks if user exists and if service is not already subscribed.
        If all checks are negative then it adds new service name to a list of subscribed services and updates database
        :param username: dict type object that consists of searched value
        :param service_name: name of service to subscribe
        :return: None
        """
        username_query = self.find({"username": username})
        if not username_query:
            raise UsernameDoesntExists
        service_query = self.find({"service": service_name})
        if not service_query:
            raise ServiceDoesntExists
        if service_name not in (services := username_query["services"]):
            services.append(service_name)
            updated_query = {"username": username, "services": services}
        else:
            raise ServiceIsAlreadySubscribed
        self.collection.update_one({"username": username}, {"$set": updated_query})

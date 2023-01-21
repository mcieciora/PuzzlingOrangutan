class UsernameDoesntExists(Exception):
    """Username does not exist."""


class UsernameAlreadyExists(Exception):
    """Username already exists."""


class ServiceIsAlreadySubscribed(Exception):
    """Service is already subscribed by user."""


class ServiceDoesntExists(Exception):
    """Service does not exist."""


class ServiceAlreadyExists(Exception):
    """Service already exists."""

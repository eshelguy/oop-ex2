from __future__ import annotations
from User import User


class SocialNetworkMeta(type):
    """SocialNetwork singleton metaclass"""

    _network: SocialNetwork = None

    def __call__(cls, *args, **kwargs):
        if SocialNetworkMeta._network is not None:
            return SocialNetworkMeta._network

        if len(args) == 1 and isinstance(args[0], str):
            name = args[0]
            SocialNetworkMeta._network = super(SocialNetworkMeta, cls).__call__(*args, **kwargs)

            print(f"The social network {name} was created!")

        return SocialNetworkMeta._network


class SocialNetwork(metaclass=SocialNetworkMeta):
    """Class representing a social network"""

    def __init__(self, name: str):
        """Constructor

        The name parameter will be used to ensure singleton functionality.

        :param name: Name of social network"""

        self._name = name
        self._users: dict[str, User] = {}

    def sign_up(self, username, password) -> User | None:
        """Register a user in the network

        :param username: Username to set
        :param password: Password to set
        :return: The created user or None if registration failed"""

        if username in self._users or len(password) < 4 or len(password) > 8:
            return None

        user = User(username, password)
        self._users[username] = user
        return user

    def log_in(self, username: str, password: str) -> bool:
        """Log in to the network

        :param username: Username of user to log in
        :param password: Password of user to log in
        :return: True if operation succeeded, else False"""

        user = self._users.get(username)
        if user is None or not user.check_password(password) or user.connected:
            return False

        user.connected = True
        print(f"{user.username} connected")
        return True

    def log_out(self, username: str) -> bool:
        """Log out of network

        :param username: Username of user to log out
        :return: True if operation succeeded, else False"""

        user = self._users.get(username)
        if user is None or not user.connected:
            return False

        user.connected = False
        print(f"{user.username} disconnected")
        return True

    @property
    def name(self) -> str:
        """Name of network"""

        return self._name

    def __str__(self):
        return f"{self.name} social network:\n" + "\n".join(map(str, self._users.values()))

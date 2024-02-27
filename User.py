from __future__ import annotations

from collections import deque
from functools import wraps

from Post import Post, TextPost, ImagePost, SalePost, NotificationType


def require_connection(func):
    @wraps(func)
    def wrapper(self: User, *args, **kwargs):
        if self.connected:
            return func(self, *args, **kwargs)

        return False

    return wrapper


class User:
    """Class representing a user in the social network"""

    def __init__(self, username, password):
        """Constructor

        :param username: Username of user to create
        :param password: Password of user to create
        """
        self._username = username
        self._password = password
        self.connected = True

        self._followers: set[User] = set()
        self._notifications: deque[str] = deque()
        self._posts: list[Post] = []

    @require_connection
    def follow(self, user: User):
        """Perform a follow operation

        :param user: User to follow
        :return: True if operation succeeded, else False"""

        if self in user._followers:
            return False
        
        user._followers.add(self)
        print(f"{self._username} started following {user._username}")
        return True

    @require_connection
    def unfollow(self, user: User):
        """Perform unfollow operation

        :param user: User to unfollow
        :return: True if operation succeeded, else False"""

        user._followers.remove(self)
        print(f"{self._username} unfollowed {user._username}")
        return True

    @require_connection
    def publish_post(self, type_: str, body: str, price: int = None, location: str = None) \
            -> TextPost | ImagePost | SalePost | None:
        """Post factory

        :param type_: Type of post
        :param body: Body of post
        :param price: Asking price of item for sale (required only for SalePosts)
        :param location: Pickup location (required only for SalePosts)
        :return: Created post"""

        types = {
            "Text": TextPost(body, self),
            "Image": ImagePost(body, self),
            "Sale": SalePost(body, price, location, self),
        }

        if type_ not in types:
            raise ValueError(f"Post type {type_} not recognized. Must be one of: {', '.join(types.keys())}")

        post = types[type_]
        self.issue_notification(NotificationType.NEW_POST)
        self._posts.append(post)

        print(post)

        return post

    def print_notifications(self):
        """Print this user's notifications"""

        print(f"{self._username}'s notifications:")
        while len(self._notifications) != 0:
            print(self._notifications.popleft())

    def check_password(self, password):
        """Compares a given password with this user's password

        :param password: Password to check
        :return: True if passwords match, else False
        """
        return self._password == password

    def issue_notification(self, type_: NotificationType, body: str = None):
        """Issue a wide notification to this user's followers (observers)

        :param type_: Type of notification to issue
        :param body: Body of notification"""

        for observer in self._followers:
            observer.notify(self, type_, body=body, direct_notification=False)

    def notify(self, initiater: User, type_: NotificationType, body: str = None, direct_notification=True):
        """Issue this user a notification

        :param initiater: User that initiated the notification
        :param type_: Notification type
        :param body: Body of notification
        :param direct_notification: True if this notification is direct, else False"""
        if initiater == self:
            return

        self._notifications.append(f"{initiater._username} {type_.value}")
        if direct_notification:
            print(f"notification to {self._username}: {initiater._username} {type_.value}" +
                  (f": {body}" if body is not None else ""))

    @property
    def username(self) -> str:
        """User's username"""
        return self._username

    def __repr__(self):
        return f"<User {self.username}>"

    def __str__(self):
        return f"User name: {self._username}, " \
               f"Number of posts: {len(self._posts)}, " \
               f"Number of followers: {len(self._followers)}"

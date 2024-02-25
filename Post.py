from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import TYPE_CHECKING

from matplotlib import pyplot as plt, image as mpimg

if TYPE_CHECKING:
    from User import User


class NotificationType(Enum):
    """Enumerated type representing notification types"""

    LIKE = "liked your post"
    COMMENT = "commented on your post"
    NEW_POST = "has a new post"


class Post(ABC):
    """Class representing a post on the social network"""

    def __init__(self, poster: User):
        """Constructor

        :param poster: User that published this post"""
        self._poster = poster

    def like(self, user: User):
        """Perform a like operation on this post

        :param user: User that initiated the operation"""
        self._poster.notify(user, NotificationType.LIKE)

    def comment(self, user: User, body: str):
        """Perform a comment operation on this post

        :param user: User that initiated the operation
        :param body: Comment body"""
        self._poster.notify(user, NotificationType.COMMENT, body)

    @abstractmethod
    def display(self):
        """Display this post"""
        pass


class TextPost(Post):
    def __init__(self, body: str, poster: User):
        """Constructor

        :param body: Body of post
        :param poster: User that published this post"""

        super().__init__(poster)
        self._body = body

    def display(self):
        print(self._body)

    @property
    def body(self):
        """Body of this post"""
        return self._body

    def __repr__(self):
        return f"<TextPost \"{self._body[:50]}\" {self._poster.username}>"

    def __str__(self):
        return f"""{self._poster.username} published a post:
\"{self._body}\"
"""


class ImagePost(Post):
    def __init__(self, image_path: str, poster: User):
        """Constructor

        :param image_path: Path to image file
        :param poster: User that published this post"""

        super().__init__(poster)
        self._image_path = image_path

    def display(self):
        print("Shows picture")
        image = mpimg.imread(self._image_path)
        plt.imshow(image)
        plt.title(self._image_path)
        plt.axis("off")
        plt.show()

    def __repr__(self):
        return f"<ImagePost {self._image_path} {self._poster.username}>"

    def __str__(self):
        return f"{self._poster.username} posted a picture\n"


class SalePost(Post):
    def __init__(self, title: str, price: int, location: str, poster: User):
        """Constructor

        :param title: Title of post
        :param price: Asking price of item for sale
        :param location: Pickup location
        :param poster: User that published this post"""

        super().__init__(poster)
        self._title = title
        self._price = price
        self._location = location
        self._sold = False

    def sold(self, password: str):
        """Set this sale as completed

        :param password: Password of post publisher
        :return: True if operation succeeded, else False"""

        if not self._poster.check_password(password):
            return False

        self._sold = True
        print(f"{self._poster.username}'s product is sold")
        return True

    def discount(self, percent: int, password: str):
        """Apply a percentage discount to this sale

        :param percent: Discount percentage
        :param password: Password of post publisher
        :return: True if operation succeeded, else False"""

        if not self._poster.check_password(password) or self._sold:
            return False

        self._price -= self._price / percent
        print(f"Discount on {self._poster.username} product! the new price is: {self._price}")
        return True

    def display(self):
        print(self._sold)

    @property
    def price(self):
        """Price"""
        return self._price

    def __repr__(self):
        return f"<SalePost \"{self._title}\" {self._price} {self._location} {self._poster.username}>"

    def __str__(self):
        return f"""{self._poster.username} posted a product for sale:
{'Sold' if self._sold else 'For sale'}! {self._title}, price: {self._price}, pickup from: {self._location}
"""

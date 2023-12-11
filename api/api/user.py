"""
Module: user.py

This module defines the User class representing a user in the application.
"""


class User:
    """
    Defines the User class representing a user in the application.
    """

    def __init__(self, username: str, access_token: str) -> None:
        """
        Initializes a new User instance with the provided username and access token.

        Parameters:
            - username (str): The username of the user.
            - access_token (str): The access token associated with the user.
        """
        self.username = username
        self.access_token = access_token

    def __str__(self) -> str:
        """
        Returns a string representation of the User object, which is the username.

        Returns:
            str: The username of the user.
        """
        return self.username

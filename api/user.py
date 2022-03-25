

class User:
    """Defines the user"""

    def __init__(self, username: str, access_token: str) -> None:
        self.username = username
        self.access_token = access_token

    def __str__(self) -> str:
        return self.username

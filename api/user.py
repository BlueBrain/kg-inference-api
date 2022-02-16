

class User:
    """Defines the user"""

    def __init__(self, username: str) -> None:
        self.username = username

    def __str__(self) -> str:
        return self.username

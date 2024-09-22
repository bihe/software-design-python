from dataclasses import dataclass


@dataclass
class User:
    id: str
    display_name: str
    email: str

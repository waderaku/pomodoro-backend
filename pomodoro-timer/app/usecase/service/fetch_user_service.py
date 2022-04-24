from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    is_google_linked: bool
    google_config: dict | None
    default_length: dict


def fetch_user_service(user_id: str) -> User:
    pass

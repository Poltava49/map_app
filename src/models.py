from dataclasses import dataclass


@dataclass
class AppState:
    pass


@dataclass
class SearchHistory:
    full_adress: str
    toponym_longitude: str
    toponym_lattitude: str
    adress_index: str


@dataclass
class UserAttributes:
    name: str
    login: str
    password: str

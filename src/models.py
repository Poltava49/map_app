from dataclasses import dataclass


@dataclass
class AppState:
    pass


@dataclass
class SearchResult:
    full_adress: str
    toponym_longitude: str
    toponym_lattitude: str
    adress_index:  str | None = None


@dataclass
class SearchHistory:
    user_id: int
    search_query: str


@dataclass
class UserAttributes:
    name: str
    login: str
    password: str

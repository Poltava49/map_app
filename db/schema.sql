CREATE TABLE IF NOT EXISTS users
(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(30) NOT NULL,
);

CREATE TABLE IF NOT EXISTS search_history
(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    serch_query VARCHAR(255) NOT NULL,

    FOREIGN KEY (user_id)
  	REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS favorites
(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    coords VARCHAR(20) NOT NULL,
    full_address VARCHAR(255) NOT NULL,
    orgainsation_name VARCHAR(255) NULL DEFAULT NULL

    FOREIGN KEY (user_id)
  	REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS cache
(
    id INTEGER PRIMARY KEY,
    request_url TEXT NOT NULL,
    request_body TEXT NULL,
    resposne_status_code INTEGER NOT NULL,
    respose_body TEXT NULL,
    is_file BOOLEAN NOT NULL,
    file_name VARCHAR(40) NULL,
)

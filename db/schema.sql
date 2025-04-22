-- users определение

CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    login VARCHAR(255) NOT NULL,
    password VARCHAR(30) NOT NULL,
    FOREIGN KEY (user_id)
  	REFERENCES search_binary(user_id)
);

-- search_history определение

CREATE TABLE search_history
(
    user_id INTEGER,
    name VARCHAR(255),
    history VARCHAR(255),
    coords VARCHAR(255),
    FOREIGN KEY (user_id)
  	REFERENCES users(user_id)
);
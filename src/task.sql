-- Table: user
DROP TABLE IF EXISTS user;
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Table: status
DROP TABLE IF EXISTS status;
CREATE TABLE status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);


-- Table: tasks 
DROP TABLE IF EXISTS tasks;
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status (id)
      ON DELETE SET NULL
      ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES user (id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
);

-- Заповнення таблиці status початковими даними
INSERT INTO status (name) VALUES 
    ('new'),
    ('in progress'),
    ('completed');
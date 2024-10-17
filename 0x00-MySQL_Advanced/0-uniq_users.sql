-- An SQL script that creates a table with unique users.
-- The table should have the following columns:
-- 1. id - an integer that is the primary key of the table.
-- 2. name - a string that is the name of the user.
-- 3. email - a string that is the email of the user.

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
)

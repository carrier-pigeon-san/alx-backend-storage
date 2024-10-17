-- An SQL script that creates a table users with the following columns:
-- 1. id - an integer that is the primary key of the table.
-- 2. email - a string that is the email of the user.
-- 3. name - a string that is the name of the user.
-- 4. country - a string that is the country of the user.
-- The email column should be unique.
-- The country column should have a default value of 'US'.
-- The name column should not be nullable.
-- The country column should not be nullable.
-- The table should be created in the default database.
-- The table should be named users.

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
    country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
)

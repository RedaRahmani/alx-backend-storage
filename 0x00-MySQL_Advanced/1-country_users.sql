-- Sript that create users table 
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT,
    email VARCHAR(255),
    name VARCHAR(255),
    country ENUM('US','CO','TN') NOT NULL?
    PRIMARY KEY (id)
);
--SQL script create a users table
CREATE TABLE users(
    id INT NOT NULL AUTO_INCREMENT,
    email varchar(255) NOT NULL UNIQUE,
    name varchar(255),
    PRIMARY KEY (id)
);
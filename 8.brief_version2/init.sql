CREATE DATABASE IF NOT EXISTS pricedb;
USE pricedb;

-- Table des jeux
CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    urlgame VARCHAR(255) UNIQUE NOT NULL,
    game VARCHAR(100) UNIQUE NOT NULL
);

-- Table des prix
CREATE TABLE prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL ,
    price DECIMAL(10,2) NOT NULL,
    dateprice DATETIME NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id)
);

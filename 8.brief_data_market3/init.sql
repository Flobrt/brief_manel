CREATE DATABASE IF NOT EXISTS produitsdb;
USE produitsdb;

CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    brands VARCHAR(255),
    utilisateur_id INT,
    product_name VARCHAR(255),
    nutrition_grades VARCHAR(10),
    ecoscore_grade VARCHAR(10),
    lang VARCHAR(10),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
);

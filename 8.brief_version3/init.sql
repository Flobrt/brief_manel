-- Table des jeux
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    urlgame VARCHAR(255) UNIQUE NOT NULL,
    game VARCHAR(100) UNIQUE NOT NULL
);

-- Table des prix
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    game_id INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    dateprice TIMESTAMP NOT NULL,
    FOREIGN KEY (game_id) REFERENCES games(id)
);

INSERT INTO games (urlgame, game) VALUES
('https://www.instant-gaming.com/en/8003-buy-celeste-pc-mac-game-steam/', 'Celeste'),
('https://www.instant-gaming.com/en/2198-buy-hollow-knight-pc-mac-steam/', 'Hollow Knight'),
('https://www.instant-gaming.com/en/4824-buy-elden-ring-pc-steam/', 'Elden ring');
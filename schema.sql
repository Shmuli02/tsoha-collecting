CREATE TABLE coin_data (
  id SERIAL PRIMARY KEY,
  name TEXT,
  description TEXT,
  country INTEGER REFERENCES country,
  value INTEGER,
  currency INTEGER REFERENCES currency,
  material INTEGER REFERENCES material,
  mintage_amount INTEGER DEFAULT NULL,
  public BOOLEAN
);

CREATE TABLE coin_library (
  id SERIAL PRIMARY KEY,
  name TEXT,
  public BOOLEAN
);

CREATE TABLE user_coin_own (
  id SERIAL PRIMARY KEY

);

CREATE TABLE user_coin_wishlist (
  id SERIAL PRIMARY KEY,
  coin_id INTEGER REFERENCES coin_data,
  user_id INTEGER REFERENCES user
);

CREATE TABLE user (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,
  password TEXT
);

CREATE TABLE country (
  id SERIAL PRIMARY KEY,
  country TEXT
);

CREATE TABLE currency (
  id SERIAL PRIMARY KEY,
  currency TEXT
);

CREATE TABLE material (
  id SERIAL PRIMARY KEY,
  material TEXT
)

INSERT INTO country (country) VALUES ('Andorra'),('Argentina'),('Austria'),('Belarus'),
('Belgium'),('Bulgaria'),('Canada'),('Croatia'),('Cuba'),
('Cyprus'),('Czech Republic'),('Denmark'),('Ecuador'),
('Estonia'),('Finland'),('France'),('Germany'),('Greece'),
('Guatemala'),('Hungary'),('Ireland'),('Isle of Man'),
('Italy'),('Japan'),('Kazakhstan'),('Latvia'),('Lithuania'),
('Luxembourg'),('Macedonia'),('Malta'),('Mexico'),('Moldova'),
('Monaco'),('Netherlands'),('Nicaragua'),('Norway'),('Paraguay'),
('Peru'),('Poland'),('Portugal'),('Romania'),('Russia'),
('San Marino'),('Serbia'),('Slovakia'),('Slovenia'),('South Korea'),
('Spain'),('Sweden'),('Switzerland'),('Turkey'),('Ukraine'),
('United Kingdom'),('USA'),('Vatican City')

INSERT INTO material (material) VALUES ('Gold'),('Silver'),('Copper–Nickel (CuNi)'),
('Nordic gold (CuZnAl)'),('German silver (CuNiZn)'),
('Bimetal: silver, gold plating'),('Bimetal: gold, silver'),
('Bimetal: CuNi, Brass'),('Bimetal: CuNi, nordic gold'),
('Bimetal: silver, nordic gold'),('Bimetal: silver, niobium'),
('Nickel'),('Nickel, bronze plating'),('Bronze'),('Copper'),
('Bimetal: silver, titanium'),('Brass'),('Palladium'),('Platinum')
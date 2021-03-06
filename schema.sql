

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT,
  password TEXT,
  admin INTEGER
);

CREATE TABLE coin_collection (
  id SERIAL PRIMARY KEY,
  name TEXT,
  description TEXT,
  public BOOLEAN,
  coins TEXT,
  author_id INTEGER REFERENCES users
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
);

CREATE TABLE coin_data (
  id SERIAL PRIMARY KEY,
  name TEXT,
  description TEXT,
  country_id INTEGER REFERENCES country,
  value INTEGER,
  currency_id INTEGER REFERENCES currency,
  material_id INTEGER REFERENCES material,
  mintage INTEGER DEFAULT NULL,
  year INTEGER,
  public BOOLEAN,
  image_url TEXT
);

CREATE TABLE coin_user_own (
  id SERIAL PRIMARY KEY,
  coin_id INTEGER REFERENCES coin_data,
  amount INTEGER,
  user_id INTEGER REFERENCES users
);


INSERT INTO country (country) VALUES ('Alankomaat'),('Albania'),('Andorra'),
('Armenia'),('Azerbaidžan'),('Belgia'),('Bulgaria'),('Espanja'),('Georgia'),
('Irlanti'),('Islanti'),('Israel'),('Italia'),('Itävalta'),('Kreikka'),
('Kroatia'),('Kypros'),('Latvia'),('Liettua'),('Luxemburg'),('Malta'),
('Moldova'),('Monaco'),('Montenegro'),('Norja'),('Pohjois-Makedonia'),
('Portugali'),('Puola'),('Ranska'),('Romania'),('Ruotsi'),('Saksa'),
('San Marino'),('Serbia'),('Slovakia'),('Slovenia'),('Suomi'),('Sveitsi'),
('Tanska'),('Tšekki'),('Turkki'),('Ukraina'),('Unkari'),('Valko-Venäjä'),
('Vatikaani'),('Venäjä'),('Viro'),('Yhdistynyt kuningaskunta');


INSERT INTO material (material) VALUES ('Gold'),('Silver'),('Copper–Nickel (CuNi)'),
('Nordic gold (CuZnAl)'),('German silver (CuNiZn)'),
('Bimetal: silver, gold plating'),('Bimetal: gold, silver'),
('Bimetal: CuNi, Brass'),('Bimetal: CuNi, nordic gold'),
('Bimetal: silver, nordic gold'),('Bimetal: silver, niobium'),
('Nickel'),('Nickel, bronze plating'),('Bronze'),('Copper'),
('Bimetal: silver, titanium'),('Brass'),('Palladium'),('Platinum');

INSERT INTO currency (currency) VALUES ('Euro');
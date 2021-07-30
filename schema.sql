CREATE TABLE collectibles (

);

CREATE TABLE coin_collection (

);

CREATE TABLE coin_data (
  id SERIAL PRIMARY KEY,
  name TEXT,
  description TEXT,
  country TEXT REFERENCES country,
  value INTEGER,
  currency TEXT REFERENCES currency,
  material TEXT REFERENCES material,
  mintage_amount INTEGER
  public BOOLEAN
);

CREATE TABLE coin_library (
  id SERIAL PRIMARY KEY,
  name TEXT
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

CREATE TABLE users (
    id serial PRIMARY KEY,
    username text NOT NULL UNIQUE,
    password_hash text NOT NULL
);

CREATE TABLE categories(
    id serial PRIMARY KEY,
    name text NOT NULL,
    user_id int NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT unique_category_per_user UNIQUE (name, user_id)
);

CREATE TABLE contacts (
    id serial PRIMARY KEY,
    first_name text NOT NULL,
    last_name text NOT NULL,
    phone_number text NOT NULL,
    email text,
    category_id int NOT NULL REFERENCES categories (id),
    user_id int NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT unique_name_per_user UNIQUE (first_name, last_name, user_id)
);
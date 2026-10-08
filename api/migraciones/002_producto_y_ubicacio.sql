CREATE TABLE ubicacion (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE producto (
    id           INTEGER PRIMARY KEY,
    codigo       TEXT NOT NULL UNIQUE,
    nombre       TEXT NOT NULL,
    precio       REAL NOT NULL CHECK (precio >= 0),
    categoria_id INTEGER NOT NULL,
    FOREIGN KEY (categoria_id) REFERENCES categoria (id) ON DELETE RESTRICT
);
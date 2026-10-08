CREATE TABLE existencia (
    producto_id  INTEGER NOT NULL,
    ubicacion_id INTEGER NOT NULL,
    cantidad     INTEGER NOT NULL DEFAULT 0 CHECK (cantidad >= 0),
    PRIMARY KEY (producto_id, ubicacion_id),
    FOREIGN KEY (producto_id)  REFERENCES producto (id)  ON DELETE RESTRICT,
    FOREIGN KEY (ubicacion_id) REFERENCES ubicacion (id) ON DELETE RESTRICT
);

CREATE TABLE movimiento (
    id           INTEGER PRIMARY KEY,
    producto_id  INTEGER NOT NULL,
    ubicacion_id INTEGER NOT NULL,
    tipo         TEXT NOT NULL CHECK (tipo IN ('entrada', 'salida')),
    cantidad     INTEGER NOT NULL CHECK (cantidad > 0),
    fecha        TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (producto_id)  REFERENCES producto (id)  ON DELETE RESTRICT,
    FOREIGN KEY (ubicacion_id) REFERENCES ubicacion (id) ON DELETE RESTRICT
);
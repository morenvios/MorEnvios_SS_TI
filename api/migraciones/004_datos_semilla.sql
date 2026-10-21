INSERT INTO categoria (id, nombre) VALUES
    (1, 'empaque'),
    (2, 'etiquetado'),
    (3, 'proteccion');

INSERT INTO ubicacion (id, nombre) VALUES
    (1, 'Almacen A'),
    (2, 'Almacen B');

INSERT INTO producto (id, codigo, nombre, precio, categoria_id) VALUES
    (1, 'PROD-001', 'Caja de carton chica', 12.5, 1),
    (2, 'PROD-002', 'Caja de carton grande', 25, 1),
    (3, 'PROD-003', 'Cinta adhesiva transparente', 18, 1),
    (4, 'PROD-004', 'Etiqueta de envio 10x15', 0.8, 2),
    (5, 'PROD-005', 'Rollo de etiquetas termicas', 95, 2),
    (6, 'PROD-006', 'Plastico burbuja 50 m', 140, 3),
    (7, 'PROD-007', 'Esquineros de carton', 6.5, 3),
    (8, 'PROD-008', 'Bolsa de envio mediana', 3.2, 1);

INSERT INTO existencia (producto_id, ubicacion_id, cantidad) VALUES
    (1, 1, 80),
    (1, 2, 40),
    (2, 1, 60),
    (3, 1, 120),
    (4, 2, 500),
    (5, 2, 25),
    (6, 1, 15),
    (7, 1, 30);

INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) VALUES
    (1, 1, 'entrada', 100),
    (1, 1, 'salida', 20),
    (1, 2, 'entrada', 40),
    (2, 1, 'entrada', 60),
    (3, 1, 'entrada', 120),
    (4, 2, 'entrada', 500),
    (5, 2, 'entrada', 25),
    (6, 1, 'entrada', 15),
    (7, 1, 'entrada', 30);

INSERT INTO producto (codigo, nombre, precio, categoria_id) VALUES
    ('PROD-009', 'Cinta de embalaje reforzada', 22.0, 1),
    ('PROD-010', 'Sobres de burbuja 15x20', 4.5, 3),
    ('PROD-011', 'Marcador industrial negro', 12.0, 2),
    ('PROD-012', 'Fleje de plastico 100 m', 85.0, 1);

INSERT INTO existencia (producto_id, ubicacion_id, cantidad) VALUES
    (9, 1, 50),
    (10, 2, 200),
    (11, 2, 30),
    (12, 1, 10);

INSERT INTO movimiento (producto_id, ubicacion_id, tipo, cantidad) VALUES
    (9, 1, 'entrada', 50),
    (10, 2, 'entrada', 200),
    (11, 2, 'entrada', 30),
    (12, 1, 'entrada', 10);
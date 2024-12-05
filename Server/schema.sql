-- schema.sql
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT NOT NULL,
    dispositivo TEXT NOT NULL,
    horas TEXT NOT NULL,
    pagina TEXT NOT NULL,
    ultimo_dispositivo TEXT
);

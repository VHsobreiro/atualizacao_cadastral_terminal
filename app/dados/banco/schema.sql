DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS acessos;

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL,
    salario TEXT,
    veiculo TEXT,
    endereco TEXT,
    casa_propria INTEGER
);

CREATE TABLE IF NOT EXISTS acessos (
    usuario TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    cargo TEXT NOT NULL
);

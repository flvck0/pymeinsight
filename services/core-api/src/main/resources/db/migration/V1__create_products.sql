CREATE TABLE products (
    id          BIGSERIAL PRIMARY KEY,
    sku         VARCHAR(40)  NOT NULL UNIQUE,
    name        VARCHAR(120) NOT NULL,
    stock       INTEGER      NOT NULL CHECK (stock >= 0),
    min_stock   INTEGER      NOT NULL CHECK (min_stock >= 0),
    price_clp   INTEGER      NOT NULL CHECK (price_clp >= 0),
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);

INSERT INTO products (sku, name, stock, min_stock, price_clp) VALUES
    ('CAF-001', 'Café de grano 1 kg',        24, 10, 12990),
    ('TE-014',  'Té verde en hojas 250 g',    6, 12,  5490),
    ('MIEL-07', 'Miel de ulmo 500 g',         3,  8,  8990),
    ('ALM-020', 'Almendras tostadas 300 g',  40, 15,  6990);

CREATE TABLE IF NOT EXISTS store.ocorens (
    id INT NOT NULL AUTO_INCREMENT,
    chavenfe VARCHAR(255) NOT NULL,
    ocor VARCHAR(255) NOT NULL,
    origem VARCHAR(255) NOT NULL,
    pedido VARCHAR(255) NOT NULL,
    created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NULL,
    deleted_at timestamp NULL,
    PRIMARY KEY (id)
)
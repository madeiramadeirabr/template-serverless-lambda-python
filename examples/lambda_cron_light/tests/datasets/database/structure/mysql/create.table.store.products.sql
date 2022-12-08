CREATE TABLE IF NOT EXISTS store.products (
    id INT NOT NULL AUTO_INCREMENT,
    uuid VARCHAR(60) NOT NULL,
    sku INT(11) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    supplier_id INT(11) NOT NULL,
    created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp NULL,
    deleted_at timestamp NULL,
    PRIMARY KEY (id)
)
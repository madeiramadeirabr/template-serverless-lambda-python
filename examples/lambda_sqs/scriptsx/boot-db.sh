echo 'Booting database...'
# TODO futuramente usar o Flask migrate ou outra alternativa

echo 'Creating tables...'
python3 ./scripts/migrations/mysql/migrate.py ./tests/datasets/database/structure/mysql/create.table.store.ocorens.sql
python3 ./scripts/migrations/mysql/migrate.py ./tests/datasets/database/structure/mysql/create.table.store.products.sql

echo 'Inserting data in the table...'
python3 ./scripts/migrations/mysql/migrate.py ./tests/datasets/database/seeders/mysql/seeder.table.store.ocorens.sql
python3 ./scripts/migrations/mysql/migrate.py ./tests/datasets/database/seeders/mysql/seeder.table.store.products.sql

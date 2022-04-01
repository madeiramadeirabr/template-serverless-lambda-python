#!/bin/bash
# -----------------------------------------------------------------------------
# Current file variables
# -----------------------------------------------------------------------------
debug=false
parent_folder="../"
current_path=$(pwd)/
current_path_basename=$(basename $(pwd))
current_file_full_path=$0
# echo $current_filepath
current_file_name=$(basename -- "$0")
# echo $current_filename
if [ $current_file_full_path = $current_file_name ] || [ $current_file_full_path = "./$current_file_name" ]; then
  current_file_full_path="./${current_file_full_path}"
  current_file_path="./"
else
  current_file_path="${current_file_full_path/$current_file_name/''}"
fi

current_file_path_basename=$(basename -- "$current_file_path")
#echo "xxxxx current_file_path_basename $current_file_path_basename"

if [ -z "$current_file_path_basename" ] || [ $current_file_path = "./" ]; then
#  echo 'aq'
  current_parent_folder="../"
else
#  echo 'naq'
  current_file_path_basename=$current_file_path_basename/
  current_parent_folder="${current_file_path/$current_file_path_basename/''}"
fi


if [ debug ]; then
  echo '----------------------------------------'
  echo "$0 - Script variables"
  echo '----------------------------------------'
  echo "current_path: $current_path"
  echo "current_path_basename: $current_path_basename"
  echo "current_file_full_path: $current_file_full_path"
  echo "current_file_name: $current_file_name"
  echo "current_file_path: $current_file_path"
  echo "current_parent_folder: $current_parent_folder"
  echo '----------------------------------------'
fi

if test -f ${current_parent_folder}/scripts/migrations/mysql/migrate.py; then
  echo '----------------------------------------'
  echo 'Booting database...'
  echo '----------------------------------------'
  # TODO futuramente usar o Flask migrate ou outra alternativa
  echo 'Creating tables...'
  python3 ${current_parent_folder}/scripts/migrations/mysql/migrate.py ${current_parent_folder}/tests/datasets/database/structure/mysql/create.table.store.ocorens.sql
  python3 ${current_parent_folder}/scripts/migrations/mysql/migrate.py ${current_parent_folder}/tests/datasets/database/structure/mysql/create.table.store.products.sql

  read -p "Press enter to continue..."

  echo 'Inserting data in the table...'
  python3 ${current_parent_folder}/scripts/migrations/mysql/migrate.py ${current_parent_folder}/tests/datasets/database/seeders/mysql/seeder.table.store.ocorens.sql
  python3 ${current_parent_folder}/scripts/migrations/mysql/migrate.py ${current_parent_folder}/tests/datasets/database/seeders/mysql/seeder.table.store.products.sql
fi



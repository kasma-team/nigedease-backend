#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE core_db;
    CREATE DATABASE user_management_db;
    GRANT ALL PRIVILEGES ON DATABASE core_db TO postgres;
    GRANT ALL PRIVILEGES ON DATABASE user_management_db TO postgres;
EOSQL 
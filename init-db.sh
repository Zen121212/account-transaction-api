#!/bin/bash
set -e

# This script runs inside the Postgres container on init
# It creates the test database and sets up tables manually

# Create the test database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE accounts_transactions_test;
EOSQL

# Connect to the test DB and create tables
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname="accounts_transactions_test" <<-EOSQL
  CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    balance NUMERIC DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );

  CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
    amount NUMERIC NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
EOSQL

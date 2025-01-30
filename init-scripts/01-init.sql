-- Create database if not exists
SELECT 'CREATE DATABASE mydatabase' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'mydatabase');

-- Connect to the database
\c mydatabase;

-- Add any additional initialization here if needed

-- Create the database
CREATE DATABASE IF NOT EXISTS face_recognition_db;
USE face_recognition_db;

-- Create the 'people' table
CREATE TABLE IF NOT EXISTS people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    encoding BLOB NOT NULL
);
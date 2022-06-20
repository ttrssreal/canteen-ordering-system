CREATE TABLE User (
    id         INTEGER     PRIMARY KEY AUTOINCREMENT,
    first_name STRING (32),
    last_name  STRING (32),
    student_id INTEGER     UNIQUE,
    password   STRING (32) 
);

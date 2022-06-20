PRAGMA foreign_keys = 0;

CREATE TABLE sqlitestudio_temp_table AS SELECT *
                                          FROM User;

DROP TABLE User;

CREATE TABLE User (
    id          INTEGER     PRIMARY KEY AUTOINCREMENT,
    first_name  STRING (32),
    last_name   STRING (32),
    student_id  INTEGER     UNIQUE,
    password    STRING (32),
    permissions INTEGER
);

INSERT INTO User (
                     id,
                     first_name,
                     last_name,
                     student_id,
                     password
                 )
                 SELECT id,
                        first_name,
                        last_name,
                        student_id,
                        password
                   FROM sqlitestudio_temp_table;

DROP TABLE sqlitestudio_temp_table;

PRAGMA foreign_keys = 1;

CREATE TABLE Order (
    order_id         INTEGER  PRIMARY KEY,
    user_id                   REFERENCES User (s_id),
    date_of_creation DATETIME,
    target_date      DATETIME
);
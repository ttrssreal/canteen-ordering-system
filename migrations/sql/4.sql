CREATE TABLE OrderProduct (
    order_id         REFERENCES [Order] (order_id),
    p_id             REFERENCES Product (p_id),
    amount   INTEGER,
    id       INTEGER PRIMARY KEY AUTOINCREMENT
);

-- SELECT p_id, amount
-- FROM "Order"
-- INNER JOIN OrderProduct
-- ON
-- "Order".order_id = OrderProduct.order_id;
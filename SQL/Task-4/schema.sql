use task_1;

create table customers (
    customer_id int primary key,
    customer_name varchar(100),
    city varchar(50),
    join_date date
);

create table orders (
    order_id int primary key,
    customer_id int,
    product_name varchar(100),
    amount decimal(10, 2),
    order_date date,
    foreign key (customer_id) references customers(customer_id)
);


INSERT INTO Customers VALUES
(1, 'John Smith', 'New York', '2023-01-15'),
(2, 'Sarah Johnson', 'Los Angeles', '2023-02-20'),
(3, 'Mike Brown', 'Chicago', '2023-03-10'),
(4, 'Emma Davis', 'Houston', '2023-04-05');

INSERT INTO Orders VALUES
(101, 1, 'Laptop', 1200.00, '2024-01-10'),
(102, 1, 'Mouse', 25.00, '2024-01-15'),
(103, 2, 'Keyboard', 75.00, '2024-01-20'),
(104, 2, 'Monitor', 300.00, '2024-02-01'),
(105, 4, 'Headphones', 50.00, '2024-02-10');


-- Get customers with their orders (only matching records)
select customers.customer_name, orders.order_id, orders.product_name, orders.amount from customers inner join orders on customers.customer_id = orders.customer_id;
+---------------+----------+--------------+---------+
| customer_name | order_id | product_name | amount  |
+---------------+----------+--------------+---------+
| John Smith    |      101 | Laptop       | 1200.00 |
| John Smith    |      102 | Mouse        |   25.00 |
| Sarah Johnson |      103 | Keyboard     |   75.00 |
| Sarah Johnson |      104 | Monitor      |  300.00 |
| Emma Davis    |      105 | Headphones   |   50.00 |
+---------------+----------+--------------+---------+
5 rows in set (0.00 sec)


-- All customers, even those without orders
select customers.customer_name, orders.order_id, orders.product_name, orders.amount from customers left join orders on customers.customer_id = orders.customer_id;
+---------------+----------+--------------+---------+
| customer_name | order_id | product_name | amount  |
+---------------+----------+--------------+---------+
| John Smith    |      101 | Laptop       | 1200.00 |
| John Smith    |      102 | Mouse        |   25.00 |
| Sarah Johnson |      103 | Keyboard     |   75.00 |
| Sarah Johnson |      104 | Monitor      |  300.00 |
| Mike Brown    |     NULL | NULL         |    NULL |
| Emma Davis    |      105 | Headphones   |   50.00 |
+---------------+----------+--------------+---------+
6 rows in set (0.00 sec)

--  All orders with customer info (similar to INNER JOIN here)
select customers.customer_name, orders.order_id, orders.product_name, orders.amount from customers right join orders on customers.customer_id = orders.customer_id;
+---------------+----------+--------------+---------+
| customer_name | order_id | product_name | amount  |
+---------------+----------+--------------+---------+
| John Smith    |      101 | Laptop       | 1200.00 |
| John Smith    |      102 | Mouse        |   25.00 |
| Sarah Johnson |      103 | Keyboard     |   75.00 |
| Sarah Johnson |      104 | Monitor      |  300.00 |
| Emma Davis    |      105 | Headphones   |   50.00 |
+---------------+----------+--------------+---------+
5 rows in set (0.00 sec)


-- Find customers with no orders (using LEFT JOIN + WHERE)
mysql> select customers.customer_name from customers left join orders on customers.customer_id = orders.customer_id where orders.order_id is null;
+---------------+
| customer_name |
+---------------+
| Mike Brown    |
+---------------+
1 row in set (0.00 sec)

-- Total spending per customer
select customers.customer_name, sum(orders.amount) as total_spent, count(orders.order_id) as total_orders from customers left join orders on customers.customer_id = orders.customer_id group by customers.customer_id, customers.customer_name;
+---------------+-------------+--------------+
| customer_name | total_spent | total_orders |
+---------------+-------------+--------------+
| John Smith    |     1225.00 |            2 |
| Sarah Johnson |      375.00 |            2 |
| Mike Brown    |        NULL |            0 |
| Emma Davis    |       50.00 |            1 |
+---------------+-------------+--------------+
4 rows in set (0.01 sec)


-- . Customers who spent over $100
select customers.customer_name, sum(orders.amount) as total_spent from customers inner join orders on customers.customer_id = orders.customer_id group by customers.customer_id, customers.customer_name having sum(orders.amount) > 100;
+---------------+-------------+
| customer_name | total_spent |
+---------------+-------------+
| John Smith    |     1225.00 |
| Sarah Johnson |      375.00 |
+---------------+-------------+
2 rows in set (0.00 sec)

--  Latest order per customer
select customers.customer_name, max(orders.order_date) as last_order_date from customers left join orders on customers.customer_id = orders.customer_id group by customers.customer_id, customers.customer_name;
+---------------+-----------------+
| customer_name | last_order_date |
+---------------+-----------------+
| John Smith    | 2024-01-15      |
| Sarah Johnson | 2024-02-01      |
| Mike Brown    | NULL            |
| Emma Davis    | 2024-02-10      |
+---------------+-----------------+
4 rows in set (0.01 sec)
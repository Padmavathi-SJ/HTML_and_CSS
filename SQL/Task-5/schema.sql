use task_1;

create table employees2 (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(50),
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE
)

INSERT INTO employees2 VALUES
(1, 'John Smith', 'Sales', 75000.00, '2020-03-15'),
(2, 'Sarah Johnson', 'Sales', 65000.00, '2021-01-10'),
(3, 'Mike Brown', 'Sales', 72000.00, '2020-09-12'),
(4, 'Emma Davis', 'IT', 85000.00, '2019-07-22'),
(5, 'James Wilson', 'IT', 90000.00, '2018-11-05'),
(6, 'Lisa Anderson', 'HR', 55000.00, '2022-02-28'),
(7, 'Robert Taylor', 'HR', 58000.00, '2021-08-14');


-- Non-correlated: inner query runs independently once
select emp_name, department, salary from employees2 where salary >  (select avg(salary) from employees);
+--------------+------------+----------+
| emp_name     | department | salary   |
+--------------+------------+----------+
| John Smith   | Sales      | 75000.00 |
| Emma Davis   | IT         | 85000.00 |
| James Wilson | IT         | 90000.00 |
+--------------+------------+----------+
3 rows in set (0.01 sec)

-- Correlated: inner query references outer query for each row
select emp_name, department, salary from employees2 e1 where salary > (select avg(salary) from employees2 e2 where e1.department = e2.department);
+---------------+------------+----------+
| emp_name      | department | salary   |
+---------------+------------+----------+
| John Smith    | Sales      | 75000.00 |
| Mike Brown    | Sales      | 72000.00 |
| James Wilson  | IT         | 90000.00 |
| Robert Taylor | HR         | 58000.00 |
+---------------+------------+----------+
4 rows in set (0.00 sec)


-- Find employees in departments with average salary > 70,000
select emp_name, department, salary from employees2 where department in (select department from employees2 group by department having avg(salary) > 70000);
+---------------+------------+----------+
| emp_name      | department | salary   |
+---------------+------------+----------+
| John Smith    | Sales      | 75000.00 |
| Sarah Johnson | Sales      | 65000.00 |
| Mike Brown    | Sales      | 72000.00 |
| Emma Davis    | IT         | 85000.00 |
| James Wilson  | IT         | 90000.00 |
+---------------+------------+----------+
5 rows in set (0.01 sec)

-- dept avg salary and diff 
mysql> select emp_name, department, salary, (select avg(salary) from employees2 e2 where e2.department = e1.department) as dept_avg_salary, salary - (select avg(salary) from employees2 e2 where e2.department = e1.department) as diff_from_avg from employees2 e1;
+---------------+------------+----------+-----------------+---------------+
| emp_name      | department | salary   | dept_avg_salary | diff_from_avg |
+---------------+------------+----------+-----------------+---------------+
| John Smith    | Sales      | 75000.00 |    70666.666667 |   4333.333333 |
| Sarah Johnson | Sales      | 65000.00 |    70666.666667 |  -5666.666667 |
| Mike Brown    | Sales      | 72000.00 |    70666.666667 |   1333.333333 |
| Emma Davis    | IT         | 85000.00 |    87500.000000 |  -2500.000000 |
| James Wilson  | IT         | 90000.00 |    87500.000000 |   2500.000000 |
| Lisa Anderson | HR         | 55000.00 |    56500.000000 |  -1500.000000 |
| Robert Taylor | HR         | 58000.00 |    56500.000000 |   1500.000000 |
+---------------+------------+----------+-----------------+---------------+
7 rows in set (0.01 sec)


-- Find employees who earn more than the highest salary in HR department
select emp_name, department, salary from employees2 where salary > ALL (select salary from employees2 where department = 'HR');
+---------------+------------+----------+
| emp_name      | department | salary   |
+---------------+------------+----------+
| John Smith    | Sales      | 75000.00 |
| Sarah Johnson | Sales      | 65000.00 |
| Mike Brown    | Sales      | 72000.00 |
| Emma Davis    | IT         | 85000.00 |
| James Wilson  | IT         | 90000.00 |
+---------------+------------+----------+
5 rows in set (0.01 sec)


-- Find departments that have at least one employee earning above 80,000
mysql> select distinct department from employees2 e1 where exists (select 1 from employees2 e2 where e2.department = e1.department and e2.salary > 80000);
+------------+
| department |
+------------+
| IT         |
+------------+
1 row in set (0.02 sec)

mysql>
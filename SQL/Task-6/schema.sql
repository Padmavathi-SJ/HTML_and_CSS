-- Find how many days/months/years each employee has worked

mysql> select emp_name, department, hire_date, datediff(curdate(), hire_date) as dasy_employed, datediff(curdate(), hire_date)/30 as months_employed, datediff(curdate(), hire_date)/365 as years_employed from employees2 order by hire_date desc;
+----------------+------------+------------+---------------+-----------------+----------------+
| emp_name       | department | hire_date  | dasy_employed | months_employed | years_employed |
+----------------+------------+------------+---------------+-----------------+----------------+
| Patricia Brown | Sales      | 2024-03-05 |           779 |         25.9667 |         2.1342 |
| Tom Wilson     | HR         | 2024-02-28 |           785 |         26.1667 |         2.1507 |
| Maria Garcia   | Sales      | 2024-01-20 |           824 |         27.4667 |         2.2575 |
| David Lee      | IT         | 2023-11-15 |           890 |         29.6667 |         2.4384 |
| Jennifer Chen  | IT         | 2023-09-10 |           956 |         31.8667 |         2.6192 |
| Lisa Anderson  | HR         | 2022-02-28 |          1515 |         50.5000 |         4.1507 |
| Robert Taylor  | HR         | 2021-08-14 |          1713 |         57.1000 |         4.6932 |
| Sarah Johnson  | Sales      | 2021-01-10 |          1929 |         64.3000 |         5.2849 |
| Mike Brown     | Sales      | 2020-09-12 |          2049 |         68.3000 |         5.6137 |
| John Smith     | Sales      | 2020-03-15 |          2230 |         74.3333 |         6.1096 |
| Emma Davis     | IT         | 2019-07-22 |          2467 |         82.2333 |         6.7589 |
| James Wilson   | IT         | 2018-11-05 |          2726 |         90.8667 |         7.4685 |
+----------------+------------+------------+---------------+-----------------+----------------+
12 rows in set (0.00 sec)


-- Find employees hired within the last 30 days
select emp_name, department, hire_date from employees2 where hire_date >= date_sub(curdate(), interval 30 day) order by hire_date desc;
Empty set (0.00 sec)


-- Find employees hired in the last 6 months
 select emp_name, department, hire_date from employees2 where hire_date >= date_sub(curdate(), interval 6 month) order by hire_date desc;
Empty set (0.00 sec)


-- Display dates in different formats
SELECT emp_name, 
       hire_date,
       DATE_FORMAT(hire_date, '%M %d, %Y') AS formatted_date1,
       DATE_FORMAT(hire_date, '%W, %b %d %Y') AS formatted_date2,
       DATE_FORMAT(hire_date, '%Y-%m-%d') AS iso_format,
       DATE_FORMAT(hire_date, '%d/%m/%Y') AS uk_format
FROM employees2;
+----------------+------------+--------------------+------------------------+------------+------------+
| emp_name       | hire_date  | formatted_date1    | formatted_date2        | iso_format | uk_format  |
+----------------+------------+--------------------+------------------------+------------+------------+
| John Smith     | 2020-03-15 | March 15, 2020     | Sunday, Mar 15 2020    | 2020-03-15 | 15/03/2020 |
| Sarah Johnson  | 2021-01-10 | January 10, 2021   | Sunday, Jan 10 2021    | 2021-01-10 | 10/01/2021 |
| Mike Brown     | 2020-09-12 | September 12, 2020 | Saturday, Sep 12 2020  | 2020-09-12 | 12/09/2020 |
| Emma Davis     | 2019-07-22 | July 22, 2019      | Monday, Jul 22 2019    | 2019-07-22 | 22/07/2019 |
| James Wilson   | 2018-11-05 | November 05, 2018  | Monday, Nov 05 2018    | 2018-11-05 | 05/11/2018 |
| Lisa Anderson  | 2022-02-28 | February 28, 2022  | Monday, Feb 28 2022    | 2022-02-28 | 28/02/2022 |
| Robert Taylor  | 2021-08-14 | August 14, 2021    | Saturday, Aug 14 2021  | 2021-08-14 | 14/08/2021 |
| David Lee      | 2023-11-15 | November 15, 2023  | Wednesday, Nov 15 2023 | 2023-11-15 | 15/11/2023 |
| Maria Garcia   | 2024-01-20 | January 20, 2024   | Saturday, Jan 20 2024  | 2024-01-20 | 20/01/2024 |
| Tom Wilson     | 2024-02-28 | February 28, 2024  | Wednesday, Feb 28 2024 | 2024-02-28 | 28/02/2024 |
| Jennifer Chen  | 2023-09-10 | September 10, 2023 | Sunday, Sep 10 2023    | 2023-09-10 | 10/09/2023 |
| Patricia Brown | 2024-03-05 | March 05, 2024     | Tuesday, Mar 05 2024   | 2024-03-05 | 05/03/2024 |
+----------------+------------+--------------------+------------------------+------------+------------+
12 rows in set (0.01 sec)


-- Calculate 90-day probation end date
SELECT emp_name, hire_date,
       DATE_ADD(hire_date, INTERVAL 90 DAY) AS probation_end,
       DATE_ADD(hire_date, INTERVAL 1 YEAR) AS first_anniversary
FROM employees2;

-- Extract Date Parts
-- Find employees hired in specific year/month

 SELECT emp_name, hire_date,
       YEAR(hire_date) AS hire_year,
       MONTH(hire_date) AS hire_month,
       MONTHNAME(hire_date) AS month_name,
       DAYOFWEEK(hire_date) AS day_of_week_num,
       DAYNAME(hire_date) AS weekday_name
FROM employees2
WHERE YEAR(hire_date) = 2024;

+----------------+------------+-----------+------------+------------+-----------------+--------------+
| emp_name       | hire_date  | hire_year | hire_month | month_name | day_of_week_num | weekday_name |
+----------------+------------+-----------+------------+------------+-----------------+--------------+
| Maria Garcia   | 2024-01-20 |      2024 |          1 | January    |               7 | Saturday     |
| Tom Wilson     | 2024-02-28 |      2024 |          2 | February   |               4 | Wednesday    |
| Patricia Brown | 2024-03-05 |      2024 |          3 | March      |               3 | Tuesday      |
+----------------+------------+-----------+------------+------------+-----------------+--------------+
3 rows in set (0.01 sec)


-- Find employees hired on weekends

SELECT emp_name, hire_date, DAYNAME(hire_date) AS weekday
FROM employees2
WHERE DAYOFWEEK(hire_date) IN (1, 7);  -- 1=Sunday, 7=Saturday

+---------------+------------+----------+
| emp_name      | hire_date  | weekday  |
+---------------+------------+----------+
| John Smith    | 2020-03-15 | Sunday   |
| Sarah Johnson | 2021-01-10 | Sunday   |
| Mike Brown    | 2020-09-12 | Saturday |
| Robert Taylor | 2021-08-14 | Saturday |
| Maria Garcia  | 2024-01-20 | Saturday |
| Jennifer Chen | 2023-09-10 | Sunday   |
+---------------+------------+----------+

--  Find Oldest and Newest Employees
-- Using date functions with aggregation

SELECT 
    MIN(hire_date) AS oldest_hire_date,
    MAX(hire_date) AS newest_hire_date,
    DATEDIFF(MAX(hire_date), MIN(hire_date)) AS days_between,
    TIMESTAMPDIFF(YEAR, MIN(hire_date), MAX(hire_date)) AS years_between
FROM employees2;

+------------------+------------------+--------------+---------------+
| oldest_hire_date | newest_hire_date | days_between | years_between |
+------------------+------------------+--------------+---------------+
| 2018-11-05       | 2024-03-05       |         1947 |             5 |
+------------------+------------------+--------------+---------------+
1 row in set (0.00 sec)


--Conditional Date Filtering
-- Find employees hired during specific season
SELECT emp_name, hire_date,
       CASE 
           WHEN MONTH(hire_date) IN (12, 1, 2) THEN 'Winter'
           WHEN MONTH(hire_date) IN (3, 4, 5) THEN 'Spring'
           WHEN MONTH(hire_date) IN (6, 7, 8) THEN 'Summer'
           ELSE 'Fall'
       END AS hire_season
FROM employees2;

+----------------+------------+-------------+
| emp_name       | hire_date  | hire_season |
+----------------+------------+-------------+
| John Smith     | 2020-03-15 | Spring      |
| Sarah Johnson  | 2021-01-10 | Winter      |
| Mike Brown     | 2020-09-12 | Fall        |
| Emma Davis     | 2019-07-22 | Summer      |
| James Wilson   | 2018-11-05 | Fall        |
| Lisa Anderson  | 2022-02-28 | Winter      |
| Robert Taylor  | 2021-08-14 | Summer      |
| David Lee      | 2023-11-15 | Fall        |
| Maria Garcia   | 2024-01-20 | Winter      |
| Tom Wilson     | 2024-02-28 | Winter      |
| Jennifer Chen  | 2023-09-10 | Fall        |
| Patricia Brown | 2024-03-05 | Spring      |
+----------------+------------+-------------+
12 rows in set (0.01 sec)



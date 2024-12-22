DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS tasks;


CREATE TABLE projects(
    id INTEGER PRIMARY KEY,
project_number INTEGER(10) NOT NULL,
project_name VARCHAR(100) NOT NULL,
pm VARCHAR(100) NOT NULL
);


CREATE TABLE tasks(
    id INTEGER PRIMARY KEY,
task_number VARCHAR(3),
task_name VARCHAR(200),
task_budget INTEGER(9 , 2)
);


CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
invoice_number INTEGER (20),
invoice_month VARCHAR(15),

)
--Tables

DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS invoices;

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_number UNIQUE INTEGER NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    pm VARCHAR(100) NOT NULL
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_number VARCHAR(3) NOT NULL,
    task_name VARCHAR(200) NOT NULL,
    task_budget REAL NOT NULL
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number INTEGER NOT NULL,
    invoice_month VARCHAR(15) NOT NULL,
    invoice_year VARCHAR(15) NOT NULL,
    FOREIGN KEY (task_billed_amount) REFERENCES tasks(task_number)
);

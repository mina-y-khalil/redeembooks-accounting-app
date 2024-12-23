-- TABLES

DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS invoices;

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_number REAL UNIQUE NOT NULL,
    project_name VARCHAR(100) NOT NULL,
    cwa_number VARCHAR(100) NOT NULL,
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
    invoice_number VARCHAR(15) NOT NULL,
    invoice_month VARCHAR(15) NOT NULL,
    invoice_year INTEGER NOT NULL,
    billing_statues BOOLEAN NOT NULL DEFAULT FALSE,
    task_number VARCHAR(3) NOT NULL,
    task_billed_amount REAL NOT NULL,
    FOREIGN KEY (task_number) REFERENCES tasks(task_number)
);

-- INSERT TO TABLES
---------------------------

-- PROJECTS

INSERT INTO projects (project_number, project_name, cwa_number, pm) VALUES
(2169.01, 'this is project 01', 'CWA-01', 'John');

INSERT INTO projects (project_number, project_name, cwa_number, pm) VALUES
(2169.02, 'this is project 02', 'CWA-02', 'Scott');



-- TASKS

INSERT INTO tasks (task_number, task_name, task_budget) VALUES
('1s', 'this is task 01', 999.99);

-- INVOICES

INSERT INTO invoices (invoice_number, invoice_month, invoice_year, billing_statues, task_number, task_billed_amount) VALUES
('2169.01-1', 'DEC', 2024, 1, '1s', 556.99);

-- QUERY TO REVIEW TABLES

SELECT * FROM projects;
SELECT * FROM tasks;
SELECT * FROM invoices;

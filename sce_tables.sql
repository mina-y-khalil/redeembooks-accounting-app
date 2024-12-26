-- TABLES

DROP TABLE IF EXISTS po_number;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS invoices;

CREATE TABLE po_number (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    po NUMERIC NOT NULL
);

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
    po NUMERIC NOT NULL,
    FOREIGN KEY (task_number) REFERENCES tasks(task_number)
    FOREIGN KEY (po) REFERENCES po_number(po)
);

-- INSERT TO TABLES
---------------------------

-- PO NUMBER

INSERT INTO po_number (po) VALUES
(123456789);


-- PROJECTS

INSERT INTO projects (project_number, project_name, cwa_number, pm) VALUES
(2169.01, 'this is project 01', 'CWA-01', 'John');

INSERT INTO projects (project_number, project_name, cwa_number, pm) VALUES
(2169.02, 'this is project 02', 'CWA-02', 'Scott');



-- TASKS

INSERT INTO tasks (task_number, task_name, task_budget) VALUES
('01s', 'this is task 01', 999.99);

-- INVOICES

INSERT INTO invoices (invoice_number, invoice_month, invoice_year, billing_statues, task_number, task_billed_amount, po) VALUES
('2169.01-1', 'DEC', 2024, 1, '01S', 556.99, 123456789);

-- QUERY TO REVIEW TABLES

SELECT * FROM po_number;
SELECT * FROM projects;
SELECT * FROM tasks;
SELECT * FROM invoices;
SELECT * FROM invoices ORDER BY invoice_number DESC;
SELECT * FROM invoices WHERE invoice_month = "DEC";
-- SELECT * FROM invoices WHERE invoice_month = "DEC" AND LENGHT(invoice_month) > 5;
SELECT * FROM invoices WHERE invoice_number LIKE "%2169";
-- SELECT * FROM invoices WHERE invoice_year IN (2024 , 2025);
-- SELECT * FROM invoices WHERE invoice_year BETWEEN 2024 AND 2025;
-- SELECT * FROM invoices LIMIT 5 OFFESET 5 ;


--  UPDATE
-- UPDATE FROM invoices SET invoice_number = "1234.01" WHERE invoice_month LIKE"%DEC "


-- DELETE
-- DELETE FROM projects WHERE invoice_month = "OCT";
-- DELETE FROM projects WHERE invoice_month LIKE "%OCT";


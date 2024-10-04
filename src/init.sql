-- Create Customers Table
CREATE TABLE customers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  phone VARCHAR(20),
  address TEXT,
  created_on TIMESTAMP NOT NULL DEFAULT NOW(),
  modified_on TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Sample Data for Customers Table
INSERT INTO customers (id, name, email, phone, address)
VALUES
('44444444-4444-4444-4444-444444444444', 'Alice Johnson', 'alice.johnson@example.com', '456-789-0123', '123 Maple St'),
('55555555-5555-5555-5555-555555555555', 'Charlie Brown', 'charlie.brown@example.com', '567-890-1234', '456 Pine St'),
('66666666-6666-6666-6666-666666666666', 'Diana Prince', 'diana.prince@example.com', '678-901-2345', '789 Willow St'),
('77777777-7777-7777-7777-777777777777', 'Evan Chen', 'evan.chen@example.com', '789-012-3456', '123 Birch St'),
('88888888-8888-8888-8888-888888888888', 'Fiona Apple', 'fiona.apple@example.com', '890-123-4567', '456 Oak St'),
('99999999-9999-9999-9999-999999999999', 'George Orwell', 'george.orwell@example.com', '901-234-5678', '789 Walnut St'),
('10101010-1010-1010-1010-101010101010', 'Hermione Granger', 'hermione.granger@example.com', '012-345-6789', '123 Spruce St');


-- Create Jobs Table
CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(100) NOT NULL CHECK (status IN ('Pending', 'In Progress', 'Complete', 'Cancelled')),
  created_by VARCHAR(255) NOT NULL,
  created_on TIMESTAMP NOT NULL DEFAULT NOW(),
  modified_on TIMESTAMP NOT NULL DEFAULT NOW(),
  customer_id UUID REFERENCES customers(id),
  due_date DATE,
  priority VARCHAR(50) CHECK (priority IN ('Low', 'Medium', 'High'))
);

-- Sample Data for Jobs Table
INSERT INTO jobs (name, description, status, created_by, customer_id)
VALUES
('Job 4', 'Description for Job 4', 'Pending', 'Alice Johnson', '44444444-4444-4444-4444-444444444444'),
('Job 5', 'Description for Job 5', 'In Progress', 'Charlie Brown', '55555555-5555-5555-5555-555555555555'),
('Job 6', 'Description for Job 6', 'Complete', 'Diana Prince', '66666666-6666-6666-6666-666666666666'),
('Job 7', 'Description for Job 7', 'Cancelled', 'Evan Chen', '77777777-7777-7777-7777-777777777777'),
('Job 8', 'Description for Job 8', 'Pending', 'Fiona Apple', '88888888-8888-8888-8888-888888888888'),
('Job 9', 'Description for Job 9', 'In Progress', 'George Orwell', '99999999-9999-9999-9999-999999999999'),
('Job 10', 'Description for Job 10', 'Complete', 'Hermione Granger', '10101010-1010-1010-1010-101010101010');

-- Create Materials Table
CREATE TABLE materials (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  cost DECIMAL(10, 2) NOT NULL
);

-- Create Job Materials Table
CREATE TABLE job_materials (
  job_id INT REFERENCES jobs(id),
  material_id INT REFERENCES materials(id),
  quantity INT NOT NULL,
  PRIMARY KEY (job_id, material_id)
);

-- Create Invoices Table
CREATE TABLE invoices (
  id SERIAL PRIMARY KEY,
  job_id INT REFERENCES jobs(id),
  amount DECIMAL(10, 2) NOT NULL,
  status VARCHAR(50) CHECK (status IN ('Pending', 'Paid', 'Overdue')),
  issued_on TIMESTAMP NOT NULL DEFAULT NOW(),
  due_on TIMESTAMP NOT NULL
);

-- Create Employees Table
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  role VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL
);

-- Create Job Assignments Table
CREATE TABLE job_assignments (
  job_id INT REFERENCES jobs(id),
  employee_id INT REFERENCES employees(id),
  assigned_on TIMESTAMP NOT NULL DEFAULT NOW(),
  PRIMARY KEY (job_id, employee_id)
);

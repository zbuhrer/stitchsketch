CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  status VARCHAR(100) NOT NULL CHECK (status IN ('In Progress', 'Completed', 'Cancelled')),
  created_by VARCHAR(255) NOT NULL,
  created_on TIMESTAMP NOT NULL DEFAULT NOW(),
  modified_on TIMESTAMP NOT NULL DEFAULT NOW()
);

INSERT INTO jobs (name, status, created_by)
VALUES
('Job 1', 'In Progress', 'John Doe'),
('Job 2', 'Completed', 'Jane Smith'),
('Job 3', 'Cancelled', 'Bob Johnson');

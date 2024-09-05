# User & Project Management Services

## **User Management Service (UMS)**

### **API Endpoints**

- **POST /register**
  - Request body:
    ```json
    {
      "username": "<string>",
      "email": "<string>",
      "password": "<string>"
    }
    ```
  - Response: `{ message: 'User registered successfully' }` or error details

- **POST /login**
  - Request body:
    ```json
    {
      "username_or_email": "<string>",
      "password": "<string>"
    }
    ```
  - Response:
    ```json
    {
      "token": "<JWT_TOKEN>",
      "user": { ...user details... }
    }
    ```
  or error details

- **GET /profile**
  - Query parameter: `?include=[fields]` (e.g., `include=bio,profile_picture`)
  - Response: `{ user: {...user details...} }` or error details

- **PUT /profile** (update user profile)
  - Request body:
    ```json
    {
      "field": "<string>",
      "value": "<string>"
    }
    ```
  - Response: `{ message: 'Profile updated successfully' }` or error details

- **DELETE /account**
  - Response: `{ message: 'Account deleted successfully' }` or error details

### **Database Schema**

- Users table:
  ```sql
  CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
  );
  ```

- Profiles table (optional):
  ```sql
  CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    bio TEXT,
    profile_picture VARCHAR(255)
  );
  ```

## **Project Management Service (PMS)**

### **API Endpoints**

- **POST /projects**
  - Request body:
    ```json
    {
      "title": "<string>",
      "description": "<string>"
    }
    ```
  - Response: `{ project: {...project details...} }` or error details

- **GET /projects**
  - Query parameter: `?status=<STATUS>` (e.g., `?status=in_progress`)
  - Response: `[{...project details...}, {...}, ...]` or error details

- **GET /projects/{id}** (get project details)
  - Response: `{ project: {...project details...} }` or error details

- **PUT /projects/{id}**
  - Request body:
    ```json
    {
      "field": "<string>",
      "value": "<string>"
    }
    ```
  - Response: `{ message: 'Project updated successfully' }` or error details

- **DELETE /projects/{id}**
  - Response: `{ message: 'Project deleted successfully' }` or error details

### **Database Schema**

- Projects table:
  ```sql
  CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
  );
  ```

- ProjectHistory table (optional):
  ```sql
  CREATE TABLE project_history (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    event_type VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
  );
  ```

### **Class Diagram**

Here's a proposed class diagram for the User Management Service and Project Management Service using Mermaid syntax:

```mermaid
classDiagram

class User {
  -id: Integer { primaryKey }
  -username: String { unique }
  -email: String { unique }
  -password_hash: String { notNull }
  -created_at: DateTime { default NOW() }
  -updated_at: DateTime { default NOW() }

  +-- Profile : profiles
}

class Profile {
  -id: Integer { primaryKey }
  -- user_id: Integer { references users(id) }
  -bio: String?
  -profile_picture: String?
}

class Project {
  -id: Integer { primaryKey }
  -- user_id: Integer { references users(id) }
  -title: String { notNull }
  -description: String?
  -status: String { default 'pending' }

  +-- ProjectHistory : project_history
}

class ProjectHistory {
  -id: Integer { primaryKey }
  -- project_id: Integer { references projects(id) }
  -event_type: String { notNull }
  -timestamp: DateTime { default NOW() }
}

User "1" -- "*" Profile: has_one
Project "1" -- "*" ProjectHistory: has_many
```

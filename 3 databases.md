##### To run PostgreSQL, MongoDB, and MySQL using Docker Compose and insert some dummy data automatically upon container startup, you can use initialization scripts like init.sql for PostgreSQL and MySQL, and init.js for MongoDB. Docker provides a way to execute initialization scripts by placing them in the appropriate directory or using the correct Docker image environment variables.

#### 1. Create a docker-compose.yml file:
You will create a docker-compose.yml file that defines the services for PostgreSQL, MongoDB, and MySQL. In addition, you will mount initialization files to each service to automatically insert data.

```
version: '3.8'

services:
  # PostgreSQL Service
  postgres:
    image: postgres:latest
    container_name: postgres_db
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: adminpassword
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    volumes:
      - ./postgres-init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: always

  # MongoDB Service
  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - ./mongo-init.js:/docker-entrypoint-initdb.d/init.js
    restart: always

  # MySQL Service
  mysql:
    image: mysql:latest
    container_name: mysql_db
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: userpassword
    ports:
      - "3306:3306"
    volumes:
      - ./mysql-init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: always

volumes:
  postgres_data:
  mongo_data:
  mysql_data:
  ```
  
#### 2. Create Initialization Scripts:
a. PostgreSQL Initialization (postgres-init.sql)
Create a file named postgres-init.sql in the same directory as your docker-compose.yml file. This SQL script will be automatically executed when PostgreSQL starts.

```
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(50),
    salary DECIMAL
);

INSERT INTO employees (name, position, salary) VALUES
('John Doe', 'Developer', 60000),
('Jane Smith', 'Designer', 55000),
('Bob Johnson', 'Manager', 75000);
```
##### b. MongoDB Initialization (mongo-init.js)
Create a file named mongo-init.js in the same directory. This script will initialize MongoDB with some dummy data.

```
db = db.getSiblingDB('mydb'); // Switch to 'mydb'

db.createCollection('employees');

db.employees.insertMany([
    { name: "Alice", position: "Developer", salary: 70000 },
    { name: "David", position: "Marketing", salary: 45000 },
    { name: "Eva", position: "HR", salary: 50000 }
]);
```
##### c. MySQL Initialization (mysql-init.sql)
Create a file named mysql-init.sql to initialize MySQL with a table and dummy data.

```
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    position VARCHAR(50),
    salary DECIMAL(10, 2)
);

INSERT INTO employees (name, position, salary) VALUES
('Chris Evans', 'Salesperson', 50000),
('Mia Wang', 'Support', 45000),
('Jake Miles', 'Engineer', 70000);
```
#### 3. Run the Setup
Now that everything is set up:

##### 1.Build and start the Docker containers: Navigate to the directory containing your docker-compose.yml file and run:

```
docker-compose up -d
```
##### 2.Verify that the data was inserted:

PostgreSQL:

Connect to PostgreSQL using psql:
```
docker exec -it postgres_db psql -U admin -d mydb
Run:
```
SELECT * FROM employees;
```
MongoDB:

Connect to MongoDB using the mongo shell:
```
docker exec -it mongodb mongo
```
Switch to mydb and query the data:
```
use mydb;
db.employees.find().pretty();
```
MySQL:

Connect to MySQL using the MySQL CLI:
```
docker exec -it mysql_db mysql -u user -p
Run:
```
USE mydb;
SELECT * FROM employees;
```
##### Summary:
Docker Compose defines services for PostgreSQL, MongoDB, and MySQL.
Initialization scripts (init.sql for PostgreSQL and MySQL, init.js for MongoDB) are mounted and executed automatically on container startup.
Dummy data is inserted into the databases as part of the initialization process.
This setup will automatically create the databases, insert tables/collections, and load the dummy data.

### Steps

1. `docker-compose up `

2. test your connectivity with dbeaver 

3. connect to the database with command below 

```bash
docker exec -it postgres_db psql -U myuser -d mydatabase 
```

4. use the command below to create dummy table and dummy data

```bash

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
);

INSERT INTO users (name, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com'),
    ('Charlie', 'charlie@example.com');


```
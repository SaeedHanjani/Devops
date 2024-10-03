# Backup and restore Postgres DB in Docker Compose!
How we can Backup and restore Postgres DB in Docker Compose!

To create and run a PostgreSQL database using Docker Compose, you'll need to:

1. Create a docker-compose.yml file that defines the PostgreSQL service.
2. Run Docker Compose to bring up the container.

Here’s a step-by-step guide:

#### Step 1: Create a docker-compose.yml file
Create a docker-compose.yml file to define the PostgreSQL service. Here's a simple example:

```
version: '3.8'
services:
  db:
    image: postgres:latest
    container_name: postgres-db
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
```

#### Step 2: Create the init.sql file to insert dummy data
In the same directory as your docker-compose.yml file, create an init.sql file with SQL commands to create tables and insert dummy data. For example:

```
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
This script will:

Create a users table.
Insert three rows of dummy data.

#### Step 3: Run Docker Compose
In your terminal, navigate to the directory where your docker-compose.yml and init.sql files are located, then run:

```
docker-compose up
```
This will spin up the PostgreSQL container and run the init.sql file to insert the dummy data.

#### Step 4: Verify the dummy data
Once the container is running, you can connect to the PostgreSQL instance to verify that the data has been inserted. Use a PostgreSQL client like psql or a tool like DBeaver, or you can also exec into the running container and query the database using the following command:
```
docker exec -it postgres-db psql -U myuser -d mydb
```

Then, run a query to check the data:

```
SELECT * FROM users;
```

This setup will create a PostgreSQL instance with dummy data in the users table. Let me know if you need further customization!

#### To view the latest table (or any table) in DBeaver, follow these steps:

#### Step 1: Open DBeaver and Connect to Your PostgreSQL Database
1. Launch DBeaver.
2. If you don't already have a connection, create a new connection:
Click on the New Database Connection button or go to File > New > Database Connection.
Choose PostgreSQL from the list.
Enter your Host, Port (default is 5432), Database name, Username, and Password.
Click Finish to connect to the database.
#### Step 2: Open Database Navigator to Explore Tables
1. In the Database Navigator (usually located on the left-hand side), expand the connection for your PostgreSQL database.
2. Expand the Schemas section (typically "public" if you haven't created custom schemas).
3. Inside the schema, you will see folders like Tables, Views, Functions, etc. Expand the Tables folder to see all the tables in your database.
#### Step 3: View the Latest Table Data
1. Find the table you want to view in the Tables list.
2. Right-click on the table name and select View Data > All Rows.
.  Alternatively, you can use View Data > First 200 Rows if you're only interested in a quick glance at the top rows.
3. DBeaver will display the data from the selected table in the main panel.
#### Step 4: Check Timestamp or Created Date (If Applicable)
.  If you're trying to see the most recently created or updated table, you'll need to have a timestamp or a column that tracks created_at or updated_at values.
.  You can run a query in DBeaver to see the latest entries in a table based on a timestamp column. For example:
```
SELECT * FROM your_table_name
ORDER BY created_at DESC
LIMIT 1;
```

This will show the most recent row based on the created_at column. Adjust the column name based on your schema.


##### Backing up a PostgreSQL database running in a Docker container using Docker Compose is simple with the pg_dump command. You can either run the command from inside the container or from your host machine. Here’s a step-by-step guide on how to back up your PostgreSQL database in Docker Compose:

#### Step 1: Identify Your PostgreSQL Container Name
First, make sure your PostgreSQL container is running by checking the container name. You can find it by running:

```
docker ps
```
Look for the container running the PostgreSQL image (e.g., postgres) in the list. The container name will be important when performing the backup.

#### Step 2: Backup from Inside the PostgreSQL Container
You can use the docker exec command to execute pg_dump inside the running container.

Here’s how you can perform a backup:

```
docker exec -t <container_name> pg_dump -U <your_username> <your_database_name> > /path/to/backup/file.sql
```
- <container_name>: The name of your running PostgreSQL container (e.g., postgres-db).
- <your_username>: The PostgreSQL username (e.g., postgres).
- <your_database_name>: The name of the database you want to back up.
- /path/to/backup/file.sql: The path on your host machine where you want to save the backup file.
For example:
```
docker exec -t postgres-db pg_dump -U postgres mydb > /home/user/backups/mydb_backup.sql
```
This command will generate the SQL backup file in /home/user/backups/mydb_backup.sql on your host machine.

#### Step 3: Backup to a Custom Format (Optional)
If you prefer a custom format backup (for flexible restoration), you can run:

```
docker exec -t <container_name> pg_dump -U <your_username> -F c <your_database_name> > /path/to/backup/file.backup
```
For example:
```
docker exec -t postgres-db pg_dump -U postgres -F c mydb > /home/user/backups/mydb_backup.backup
```
This will create a compressed binary backup file.

#### Step 4: Backup Using Docker Volumes
If you’ve set up your Docker Compose with mounted volumes, you can directly access the data outside the container. Here's an example:

In your docker-compose.yml, make sure you have a volume set up for the PostgreSQL data, like this:

```
services:
  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
      POSTGRES_DB: mydb
    volumes:
      - ./db_data:/var/lib/postgresql/data
```
Use the pg_dump command from within the container or from the host (through the Docker volumes) to back up the database.

#### Step 5: Backup from Host Machine with Docker Compose Command
Alternatively, you can use Docker Compose to perform the backup without directly entering the container:

```
docker-compose exec <service_name> pg_dump -U <your_username> <your_database_name> > /path/to/backup/file.sql
```
For example:

```
docker-compose exec db pg_dump -U postgres mydb > /home/user/backups/mydb_backup.sql
```
Here, db is the service name from your docker-compose.yml.

#### Step 6: Automate Backup with a Script (Optional)
If you want to automate the backup process, you can create a shell script like this:
```
#!/bin/bash
BACKUP_PATH="/home/user/backups"
DATE=$(date +%Y%m%d_%H%M%S)
CONTAINER_NAME="postgres-db"
DB_NAME="mydb"
DB_USER="postgres"

docker exec -t $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > $BACKUP_PATH/${DB_NAME}_$DATE.sql
echo "Backup completed: ${BACKUP_PATH}/${DB_NAME}_$DATE.sql"
```

Make it executable:
```
chmod +x backup.sh
```
Then, run the script:

```
./backup.sh
```
#### Step 7: Restore the Backup
To restore a PostgreSQL database from a backup file, you can use the following command:

```
docker exec -i <container_name> psql -U <your_username> -d <your_database_name> < /path/to/backup/file.sql
```
For example:

```
docker exec -i postgres-db psql -U myuser -d mydb < /home/root/backups/mydb_backup.sql
```

#### Delete a Specific Database Inside PostgreSQL
You can delete a specific database inside a PostgreSQL instance running in Docker Compose by using the psql command. Here’s how to do it:

#### Step 1: Access the PostgreSQL Container
First, you need to access the running PostgreSQL container:

```
docker-compose exec <service_name> bash
```
For example, if your service is named db, the command would be:

```
docker-compose exec db bash
```
#### Step 2: Access the PostgreSQL Command Line
Once inside the container, access the psql prompt using the PostgreSQL user (postgres by default):

```
psql -U postgres
```
#### Step 3: Drop the Database
Inside the psql shell, you can drop the specific database using the following command:

```
DROP DATABASE <database_name>;
```
For example, if your database is named mydb, the command would be:
```
DROP DATABASE mydb;
```
Exit the psql prompt:

```
\q
```

### $ pass data in python ???
#### 1. Using $ in f-strings (formatted string literals):
Python supports f-strings (introduced in Python 3.6) for string formatting. The dollar sign can appear inside a string, but it doesn't have a special meaning in Python's f-strings.
Example:
```
python
amount = 100
formatted = f"The total is ${amount}"
print(formatted)
```
Output:
```
swift
The total is $100
```
#### 2. Using string.Template for String Substitution:
Python’s string module provides the Template class, which uses $ for string substitutions.
Example:
python
```
from string import Template
template = Template('Hello, $name!')
result = template.substitute(name='John')
print(result)
```
Output:
```
Hello, John!
```
These are the primary ways you might encounter the dollar sign in Python code!

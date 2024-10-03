# Backup and restore Postgres DB in Docker Compose!
How we can Backup and restore Postgres DB in Docker Compose!

To create and run a PostgreSQL database using Docker Compose, you'll need to:

1. Create a docker-compose.yml file that defines the PostgreSQL service.
2. Run Docker Compose to bring up the container.

Here’s a step-by-step guide:

## Step 1: Create a docker-compose.yml file
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

####To view the latest table (or any table) in DBeaver, follow these steps:

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

##### Backing up a PostgreSQL database in Linux is straightforward using the pg_dump command-line utility. Here’s how you can back up a PostgreSQL database:

#### Step 1: Ensure PostgreSQL is Installed
First, ensure that PostgreSQL and pg_dump are installed. You can check this by running:

```
pg_dump --version
```
If it’s installed, you’ll see the version number. If not, you can install PostgreSQL with:

```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

#### Step 2: Perform the Backup with pg_dump
The pg_dump command is used to back up a PostgreSQL database. Below are different ways to use it:

##### Basic Backup to a .sql File

.   pg_dump -U your_username -d your_database_name -f /path/to/backup/file.sql
.   -U your_username: The PostgreSQL username you use to connect.
.   -d your_database_name: The name of the database you want to back up.
.   -f /path/to/backup/file.sql: The file path where the backup will be saved.
For example:
```
pg_dump -U postgres -d mydb -f /home/user/backups/mydb_backup.sql
```
This command will create a SQL file that contains all the SQL commands necessary to recreate the database schema and data.

#### Full Backup of All Databases
If you want to back up all databases in the PostgreSQL instance, use pg_dumpall:

```
pg_dumpall -U your_username -f /path/to/backup/all_databases.sql
```
This will back up all the databases in the PostgreSQL instance, including roles, users, and passwords.

#### Step 4: Automate Backups with a Script (Optional)
You can automate backups by creating a shell script. Here’s a basic script to back up your database daily:

1.   Create a backup script, e.g., backup.sh:
```
#!/bin/bash
BACKUP_PATH="/home/user/backups"
DATABASE_NAME="mydb"
USER_NAME="postgres"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_PATH/${DATABASE_NAME}_$DATE.backup"

pg_dump -U $USER_NAME -d $DATABASE_NAME -F c -f $BACKUP_FILE

echo "Backup completed and saved to $BACKUP_FILE"
```

2.   Make the script executable:

```
chmod +x backup.sh
```
3.   Optionally, add the script to your crontab for periodic backups:

```
crontab -e
```
Add a line to run the backup script daily at a specified time (e.g., 2 AM):

```
0 2 * * * /path/to/backup.sh
```

This will automate the backup process.

#### Step 5: Restore the Backup (Optional)
To restore a backup, you can use the psql command for SQL files or pg_restore for custom-format backups.

##### Restore from SQL File


گام پنجم بکاپ از دامی دیتا = ok back up from database  :docker exec -t c19936495cb4  pg_dump -U myuser mydb > /file-bakcup.sql
گام پنجم بکاپ از دامی دیتا = ok 
back up from database  :docker exec -t c19936495cb4  pg_dump -U myuser mydb > /file-bakcup.sql
با پسوند بک آپ: docker exec -t <container_name> pg_dump -U <your_username> -F c <your_database_name> > /path/to/backup/file.backup
docker-compose exec db pg_dump -U myuser mydb > /home/root/backups/mydb_backup.sql

گام ششم چطور کل دیتابیس رو پاک کنم = ok
To delete a specific database inside PostgreSQL, use the DROP DATABASE command inside the PostgreSQL container:
DROP DATABASE mydb;

To delete all data, stop the containers and remove the associated Docker volumes.:
docker-compose down
docker volume rm my_project_postgres_data
docler volume ls
To completely remove the PostgreSQL service, use docker-compose down --volumes:

گام هفتم چطور بکاپم رو ری استور کنم = ok
docker exec -i postgres-db psql -U myuser -d mydb < /home/root/backups/mydb_backup.sql
https://dbeaver.io/download/
نرم افزار وصل شدن به دیتابیس های مختلف

$ pass data in python ???
1. Using $ in f-strings (formatted string literals):
Python supports f-strings (introduced in Python 3.6) for string formatting. The dollar sign can appear inside a string, but it doesn't have a special meaning in Python's f-strings.
Example:
python
amount = 100
formatted = f"The total is ${amount}"
print(formatted)
Output:
swift
The total is $100
2. Using string.Template for String Substitution:
Python’s string module provides the Template class, which uses $ for string substitutions.
Example:
python
Copy code
from string import Template
template = Template('Hello, $name!')
result = template.substitute(name='John')
print(result)
Output:
Copy code
Hello, John!
These are the primary ways you might encounter the dollar sign in Python code!

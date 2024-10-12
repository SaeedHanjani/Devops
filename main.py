import os
import click
import subprocess

# Helper functions for backup and restore
def backup_mysql():
    os.system(f"docker exec -i $(docker-compose ps -q mysql) mysqldump -u root -p rootpassword mydb > mysql_backup.sql")
    click.echo("MySQL backup completed!")

def restore_mysql():
    os.system(f"docker exec -i $(docker-compose ps -q mysql) mysql -u root -p rootpassword mydb < mysql_backup.sql")
    click.echo("MySQL restore completed!")

def backup_postgres():
    os.system(f"docker exec -i $(docker-compose ps -q postgres) pg_dump -U admin -d mydb > postgres_backup.sql")
    click.echo("PostgreSQL backup completed!")

def restore_postgres():
    os.system(f"docker exec -i $(docker-compose ps -q postgres) psql -U admin -d mydb < postgres_backup.sql")
    click.echo("PostgreSQL restore completed!")

def backup_mongo():
    os.system(f"docker exec -i $(docker-compose ps -q mongodb) mongodump --archive=mongo_backup.archive")
    click.echo("MongoDB backup completed!")

def restore_mongo():
    os.system(f"docker exec -i $(docker-compose ps -q mongodb) mongorestore --archive=mongo_backup.archive")
    click.echo("MongoDB restore completed!")


@click.command()
@click.option('--action', type=click.Choice(['backup', 'restore']), required=True, help="Action to perform: backup or restore.")
@click.option('--db', type=click.Choice(['mysql', 'postgres', 'mongo']), required=True, help="Database to perform action on.")
def main(action, db):
    if action == 'backup':
        if db == 'mysql':
            backup_mysql()
        elif db == 'postgres':
            backup_postgres()
        elif db == 'mongo':
            backup_mongo()
    elif action == 'restore':
        if db == 'mysql':
            restore_mysql()
        elif db == 'postgres':
            restore_postgres()
        elif db == 'mongo':
            restore_mongo()

if __name__ == '__main__':
    main()

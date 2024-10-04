import click
import subprocess
import os
import datetime

# Default paths
BACKUP_DIR = "./backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Utility functions
def run_docker_command(command):
    """Run a command in the PostgreSQL Docker container."""
    full_command = f"docker-compose exec db {command}"
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        click.echo(f"Error: {result.stderr}")
    return result

# Click commands
@click.group()
def cli():
    """CLI tool for PostgreSQL backup and restore"""
    pass

@cli.command()
@click.option('--filename', default=None, help="Filename to store the backup")
def backup(filename):
    """Backup PostgreSQL database to a file"""
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{BACKUP_DIR}/backup_{timestamp}.sql"

    command = f"pg_dump -U myuser -d mydatabase > {filename}"
    result = run_docker_command(command)

    if result.returncode == 0:
        click.echo(f"Backup successful! Saved as {filename}")
    else:
        click.echo(f"Backup failed: {result.stderr}")

@cli.command()
@click.argument('filepath')
def restore(filepath):
    """Restore PostgreSQL database from a backup file"""
    if not os.path.exists(filepath):
        click.echo(f"File {filepath} does not exist.")
        return

    command = f"psql -U myuser -d mydatabase < {filepath}"
    result = run_docker_command(command)

    if result.returncode == 0:
        click.echo(f"Restore successful from {filepath}")
    else:
        click.echo(f"Restore failed: {result.stderr}")

# Main entry point
if __name__ == "__main__":
    cli()

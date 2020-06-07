'''
# create_database_with_click.py
Create PostgreSQL database with Python.

Usage:
    python create_database_with_click.py -d dbname -u username
'''
import click
import subprocess


@click.command()
@click.option(
    '-d', '--database',
    default='mydb',
    prompt='Database name',
    help='Type the database name.'
)
@click.option(
    '-u', '--user',
    default='myuser',
    prompt='User name',
    help='Type the user name.'
)
def create_db(database, user):
    # Cria db
    subprocess.call(f"createdb -U postgres {database}", shell=True)
    # Cria user
    # P é para pedir senha
    # E a senha será encriptada
    subprocess.call(f"createuser -U postgres -PE {user}", shell=True)
    print('$ sudo su - postgres')
    print(f'$ psql')
    print(f'postgres=# \\l')
    print(f'ou')
    print(f'psql {database}')


if __name__ == '__main__':
    create_db()

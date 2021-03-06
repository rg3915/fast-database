'''
# create_database.py
Create PostgreSQL database with Python.

Usage:
    python create_database.py -d dbname -u username
'''
import argparse
import subprocess

description = 'Create PostgreSQL database with Python.'
parser = argparse.ArgumentParser(description=description)


parser.add_argument(
    '-d',
    '--database',
    default='mydb',
    help='Type the database name.'
)

parser.add_argument(
    '-u',
    '--user',
    default='myuser',
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
    args = parser.parse_args()
    database = vars(args)['database']
    user = vars(args)['user']
    create_db(database, user)

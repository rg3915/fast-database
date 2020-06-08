'''
Author: Regis Santos - rg3915

Insere dados no banco de dados PostgreSQL de várias formas diferentes.
Gera um benchmark para ver o método mais rápido.

Testando:

1. Django e bulk_create
2. psycopg2
3. subprocess

Requisitos:

* Instale PostgreSQL
* Gere os dados CSV previamente com
    create_database.py ou
    create_database_with_click.py

Como rodar este programa:

$ python insert_data_benchmark.py --rows 10000
'''
import click
import csv
import django
import os
import psycopg2
import subprocess
import timeit
from pathlib import Path
from typing import Iterator, Dict, Any, Optional


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myproject.core.models import Product


@click.command()
@click.option(
    '--rows',
    default='1000',
    prompt='Quantidade de linhas',
    help='Quantidade de linhas do CSV.'
)
def main(rows):
    logfile = 'time_log.txt'
    home = str(Path.home())
    filename = f'{home}/dados/produtos_{rows}.csv'

    print('-' * 40)
    print(f'> Inserindo {rows} registros.')

    data = csv_to_list(filename)

    time1 = insert_data_with_bulk_create(items=data)
    msg1 = 'Django bulk_create'
    print(time1, msg1)
    timelog(int(rows), time1, logfile, msg1)

    connection = psycopg2.connect(
        host="localhost",
        database="estoque_teste",
        user="rg3915",
        password="1234",
    )
    connection.autocommit = True

    # ATENÇÃO: método demorado, não faça isso para grandes quantidades.
    # time = insert_data_with_psycopg2_one_by_one(connection, items=data)
    # msg = 'psycopg2 one by one'
    # print(time, msg)
    # timelog(int(rows), time, logfile, msg)

    # ATENÇÃO: é tão lento quanto o one by one.
    # LENTO: 100.000 registros -> 108.931s -> 1.8 min
    # Para 14.000.605 -> 4.2 horas
    time2 = insert_data_with_psycopg2_executemany(connection, items=data)
    msg2 = 'psycopg2 executemany'
    print(time2, msg2)
    timelog(int(rows), time2, logfile, msg2)

    time3 = insert_data_with_copy_from(connection, filename)
    msg3 = 'psycopg2 copy_from'
    print(time3, msg3)
    timelog(int(rows), time3, logfile, msg3)

    print('-' * 3)
    print('bulk_create vs copy_from:', round(
        time1 / time3, 2), 'vezes mais rápido.')
    if time1 < time3:
        print('Win: Django bulk_create')
    else:
        print('Win: psycopg2 copy_from')

    print('-' * 40)

    time4 = insert_data_with_subprocess(filename)
    msg4 = 'subprocess'
    print(time4, msg4)
    timelog(int(rows), time4, logfile, msg4)

    print('-' * 3)
    print('copy_from vs subprocess:', round(
        time4 / time3, 2), 'vezes mais rápido.')
    if time3 < time4:
        print('Win: psycopg2 copy_from')
    else:
        print('Win: subprocess')

    print('-' * 40)

    smallest = min([time1, time2, time3, time4])
    if smallest == time1:
        print('Win:', time1, msg1)
    if smallest == time2:
        print('Win:', time2, msg2)
    if smallest == time3:
        print('Win:', time3, msg3)
    if smallest == time4:
        print('Win:', time4, msg4)


def csv_to_list(filename: str) -> list:
    '''
    Lê um csv e retorna um OrderedDict.
    Créditos para Rafael Henrique
    https://bit.ly / 2FLDHsH
    '''
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        csv_data = [line for line in reader]
    return csv_data


def timelog(total_items, _time, logfile, resource):
    total_items = f'{total_items:,}'.replace(',', '.')
    space = ' ' * (10 - len(total_items))
    time = round((_time), 3)
    subprocess.call(f"printf '{total_items} {space} -> {time}s\t --> Inserindo {total_items} registros com {resource}.\n' >> {logfile}", shell=True)


def insert_data_with_bulk_create(items):
    aux_list = []
    tic = timeit.default_timer()
    for item in items:
        obj = Product(title=item['title'], quantity=item['quantity'])
        aux_list.append(obj)
    Product.objects.bulk_create(aux_list)
    toc = timeit.default_timer()
    time = toc - tic
    return round((time), 3)


def insert_one_by_one(connection, items: Iterator[Dict[str, Any]]) -> None:
    with connection.cursor() as cursor:
        for item in items:
            cursor.execute("""
                INSERT INTO core_product (title, quantity)
                VALUES (
                    %(title)s,
                    %(quantity)s
                );
            """, {
                'title': item['title'],
                'quantity': int(item['quantity']),
            })


def insert_data_with_psycopg2_one_by_one(connection, items):
    tic = timeit.default_timer()
    insert_one_by_one(connection, items)  # <--- insert data
    toc = timeit.default_timer()
    time = toc - tic
    return round((time), 3)


def insert_executemany(connection, items: Iterator[Dict[str, Any]]) -> None:
    with connection.cursor() as cursor:
        all_items = [{
            'title': item['title'],
            'quantity': int(item['quantity'])
        } for item in items]

        cursor.executemany("""
            INSERT INTO core_product (title, quantity)
            VALUES (
                %(title)s,
                %(quantity)s
            );
        """, all_items)


def insert_data_with_psycopg2_executemany(connection, items):
    tic = timeit.default_timer()
    insert_executemany(connection, items)  # <--- insert data
    toc = timeit.default_timer()
    time = toc - tic
    return round((time), 3)


def insert_data_with_copy_from(connection, filename):
    tic = timeit.default_timer()
    with open(filename, 'r') as f:
        next(f)
        connection.cursor().copy_from(
            f, 'core_product', sep=',', columns=('title', 'quantity')
        )
    toc = timeit.default_timer()
    time = toc - tic
    return round((time), 3)


def insert_data_with_subprocess(filename):
    copy_sql = f"COPY core_product (title, quantity) FROM '{filename}' CSV HEADER;"
    copy_psql = f'psql -U postgres -c "{copy_sql}" estoque_teste'
    tic = timeit.default_timer()
    subprocess.call(copy_psql, shell=True)
    toc = timeit.default_timer()
    time = toc - tic
    return round((time), 3)


if __name__ == '__main__':
    main()

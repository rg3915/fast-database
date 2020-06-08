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

    if int(rows) >= 1000000:
        total_items = f'{int(rows):,}'.replace(',', '.')
        print(f'ATENÇÃO: Você está prestes a inserir {total_items} de registros.')
        continuar = input('Deseja continuar? (y/N)')
        if continuar != 'y':
            return

    print('-' * 40)
    print(f'> Inserindo {int(rows):,} registros.'.replace(',', '.'))

    print('Lendo o CSV...')
    tic0 = timeit.default_timer()
    data = csv_to_list(filename)
    toc0 = timeit.default_timer()
    time0 = toc0 - tic0
    print(round((time0), 3))

    msg1 = 'Django bulk_create'
    if int(rows) > 1000000:
        print('[X] Desativando bulk_create...')
        print('---')
        time1 = 1000
    else:
        time1 = insert_data_with_bulk_create(items=data)
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
    time2 = 10000
    msg2 = 'psycopg2 executemany'
    if int(rows) > 100000:
        if int(rows) >= 200000:
            print('[X] Desativando psycopg2 executemany...')
            print('---')
        else:
            print('ATENÇÃO: este processo é o mais lento e pode demorar horas.')
            continuar = input('Deseja continuar? (y/N)')
            if continuar == 'y':
                print('Vamos tomar um cafézinho? ;)')
                time2 = insert_data_with_psycopg2_executemany(
                    connection, items=data)
                print(time2, msg2)
                timelog(int(rows), time2, logfile, msg2)
            else:
                print('Sábia escolha. =D')

    time3 = insert_data_with_copy_from(connection, filename)
    msg3 = 'psycopg2 copy_from'
    print(time3, msg3)
    timelog(int(rows), time3, logfile, msg3)

    print(winner1(time1, time3))
    print('-' * 40)

    time4 = insert_data_with_subprocess(filename)
    msg4 = 'subprocess'
    print(time4, msg4)
    timelog(int(rows), time4, logfile, msg4)

    print(winner2(time3, time4))
    print('-' * 40)

    winner, time_winner = winner_final(
        [time1, time2, time3, time4],
        [msg1, msg2, msg3, msg4]
    )
    print('O mais rápido é:')
    print(winner)
    print(time_winner, 's')


def winner1(time1, time3):
    '''
    Retorna o campeão da primeira rodada.
    '''
    print('-' * 3)
    print('bulk_create vs copy_from:', round(
        time1 / time3, 2), 'vezes mais rápido.')
    if time1 < time3:
        return 'Win: Django bulk_create'
    return 'Win: psycopg2 copy_from'


def winner2(time3, time4):
    '''
    Retorna o campeão da segunda rodada.
    '''
    print('-' * 3)
    print('copy_from vs subprocess:', round(
        time4 / time3, 2), 'vezes mais rápido.')
    if time3 < time4:
        return 'Win: psycopg2 copy_from'
    return 'Win: subprocess'


def winner_final(times: list, msg: list) -> tuple:
    '''
    Retorna o mais rápido de todos.
    '''
    smallest = min(times)
    if smallest == times[0]:
        return msg[0], times[0]
    if smallest == times[1]:
        return msg[1], times[1]
    if smallest == times[2]:
        return msg[2], times[2]
    if smallest == times[3]:
        return msg[3], times[3]


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

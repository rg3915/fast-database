# insert_from_csv_with_bulk_create.py

import csv
import os
import sys
import django
import timeit
import subprocess
from pathlib import Path


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myproject.core.models import Product


def csv_to_list(filename: str) -> list:
    '''
    Lê um csv e retorna um OrderedDict.
    Créditos para Rafael Henrique
    https://bit.ly/2FLDHsH
    '''
    with open(filename) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        csv_data = [line for line in reader]
    return csv_data


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


def timelog(total_items, _time, logfile, resource):
    total_items = f'{total_items:,}'.replace(',', '.')
    space = ' ' * (10 - len(total_items))
    time = round((_time), 3)
    subprocess.call(f"printf '{total_items} {space} -> {time}s\t --> Inserindo {total_items} registros com {resource}.\n' >> {logfile}", shell=True)


if __name__ == '__main__':
    logfile = 'time_log.txt'

    home = str(Path.home())
    max_rows = 100000

    filename = f'{home}/dados/produtos_{max_rows}.csv'

    data = csv_to_list(filename)

    time = insert_data_with_bulk_create(data)

    print(time)

    timelog(max_rows, time, logfile, 'Django bulk_create')

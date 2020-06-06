# insert_from_csv_with_bulk_create.py

import csv
import os
import sys
import django
import timeit
import subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from myproject.core.models import Product


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


def insert_data_with_bulk_create(items):
    aux_list = []
    tic2 = timeit.default_timer()
    for item in items:
        obj = Product(title=item['produto'], quantity=item['quantidade'])
        aux_list.append(obj)
    Product.objects.bulk_create(aux_list)
    toc2 = timeit.default_timer()
    time2 = toc2 - tic2
    return round((time2), 3)


def timelog(total_items, _time, logfile):
    time = round((_time), 3)
    subprocess.call(f"printf '{total_items} \t -> {time}s\n' >> {logfile}", shell=True)


if __name__ == '__main__':
    logfile = 'time_log.txt'

    max_rows = 100000

    data = csv_to_list(f'/tmp/produtos_{max_rows}.csv')

    time2 = insert_data_with_bulk_create(data)

    print(time2)

    timelog(max_rows, time2, logfile)

'''
Cria um CSV com valores randômicos.

Usage:
    python create_csv.py --rows 100000
'''
import csv
import string
import timeit
import subprocess
from pathlib import Path
from random import choice, randint


import click
import subprocess


@click.command()
@click.option(
    '--rows',
    default='100000',
    prompt='Quantidade de linhas',
    help='Gera um arquivo CSV com valores randômicos.'
)
def main(rows):
    home = str(Path.home())
    max_rows = int(rows)

    filename = f'{home}/dados/produtos_{max_rows}.csv'
    max_digits = 12  # quantidade de dígitos de cada produto

    tic = timeit.default_timer()
    write_csv(filename, max_rows, max_digits)
    toc = timeit.default_timer()
    time = toc - tic
    print(round(time, 3), 'segundos')
    print(round((time) / 60, 3), 'minutos')
    timelog(max_rows, time, logfile)

    print('Done!')
    print('Rodar wc -l filename no terminal')
    print('Rodar head filename no terminal')


logfile = 'time_log.txt'


def gen_digits(max_length):
    return str(''.join(choice(string.ascii_letters) for i in range(max_length)))


def timelog(total_items, _time, logfile=logfile):
    total_items = f'{total_items:,}'.replace(',', '.')
    space = ' ' * (10 - len(total_items))
    time = round((_time), 3)
    subprocess.call(f"printf '{total_items} {space} -> {time}s\t --> Gerando {total_items} registros.\n' >> {logfile}", shell=True)


def write_csv(filename, max_rows, max_digits):
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['title', 'quantity'])
        for i in range(max_rows):
            csv_writer.writerow([gen_digits(max_digits), randint(100, 10000)])


if __name__ == '__main__':
    main()

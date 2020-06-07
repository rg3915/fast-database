import subprocess
import timeit
from pathlib import Path


home = str(Path.home())
max_rows = 10000

filename = f'{home}/dados/produtos_{max_rows}.csv'
logfile = 'time_log.txt'


def timelog(total_items, _time, logfile, resource):
    total_items = f'{total_items:,}'.replace(',', '.')
    space = ' ' * (10 - len(total_items))
    time = round((_time), 3)
    subprocess.call(f"printf '{total_items} {space} -> {time}s\t --> Inserindo {total_items} registros com {resource}.\n' >> {logfile}", shell=True)

# Insere os dados
copy_sql = f"COPY core_product (title, quantity) FROM '{filename}' CSV HEADER;"
copy_psql = f'psql -U postgres -c "{copy_sql}" estoque_teste'


def insert_data_with_subprocess():
    tic = timeit.default_timer()
    subprocess.call(copy_psql, shell=True)
    toc = timeit.default_timer()
    time = toc - tic
    return round((time), 3)


time = insert_data_with_subprocess()

timelog(max_rows, time, logfile, 'subprocess')

# Próximo passo: Shell script
# chmod +x insert_with_shell_script.sh
# ./insert_with_shell_script.sh

# Plus

# # Retorna os dados
# select_sql = "SELECT * FROM core_product LIMIT 5;"
# select_psql = f'psql -U postgres -c "{select_sql}" estoque_teste'
# subprocess.call(select_psql, shell=True)


# # Contando os registros
# count_sql = "SELECT COUNT(*) FROM core_product;"
# count_psql = f'psql -U postgres -c "{count_sql}" estoque_teste'
# subprocess.call(count_psql, shell=True)

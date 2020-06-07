import subprocess
import timeit


# Insere os dados
filename = '/tmp/produtos_1000.csv'  # ou produtos_14000605.csv


copy_sql = f"COPY core_product (title, quantity) FROM '{filename}' CSV HEADER;"
copy_psql = f'psql -U postgres -c "{copy_sql}" estoque_teste'


def insert_data_with_subprocess():
    tic = timeit.default_timer()
    subprocess.call(copy_psql, shell=True)
    toc = timeit.default_timer()
    print(round(toc - tic, 2), 'segundos')


insert_data_with_subprocess()

# Retorna os dados
select_sql = "SELECT * FROM core_product LIMIT 5;"
select_psql = f'psql -U postgres -c "{select_sql}" estoque_teste'
subprocess.call(select_psql, shell=True)


# Contando os registros
count_sql = "SELECT COUNT(*) FROM core_product;"
count_psql = f'psql -U postgres -c "{count_sql}" estoque_teste'
subprocess.call(count_psql, shell=True)


# In[ ]:

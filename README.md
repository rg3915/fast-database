# fast-database

Exemplo de como inserir grande quantidade de dados da forma mais rápida num banco de dados PostgreSQL.

## This project was done with:

* Python 3.8.2
* Django 2.2.13

## How to run project?

* Clone this repository.
* Create virtualenv with Python 3.
* Active the virtualenv.
* Install dependences.
* Run the migrations.

Create database:

```
# Caso exista um banco com este nome
# dropdb -U postgres estoque_teste

sudo su - postgres
psql

 CREATE ROLE rg3915 ENCRYPTED PASSWORD '1234' LOGIN;

CREATE DATABASE estoque_teste OWNER rg3915;

# Você pode se conectar no novo banco pra não precisar sair.
\c estoque_teste

\q  # sair
```


```
git clone https://github.com/rg3915/fast-database.git
cd fast-database
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

## Este projeto foi feito com:

* Python 3.8.2
* Django 2.2.13

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/fast-database.git
cd fast-database
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

## Rodando os notebooks

```
python manage.py shell_plus --notebook
```

## Usando Python e subprocess

```
import subprocess
import timeit

# Insere os dados
filename = '/tmp/produtos_14000605.csv'  # ou produtos_14000605.csv

copy_sql = f"COPY core_product (title, quantity) FROM '{filename}' CSV HEADER;"
copy_psql = f'psql -U postgres -c "{copy_sql}" estoque_teste'

tic = timeit.default_timer()
subprocess.call(copy_psql, shell=True)
toc = timeit.default_timer()
print(round(toc - tic, 2), 'segundos')
```


```
# Retorna os dados
select_sql = "SELECT * FROM core_product LIMIT 5;"
select_psql = f'psql -U postgres -c "{select_sql}" estoque_teste'
subprocess.call(select_psql, shell=True)
```


```
# Contando os registros
count_sql = "SELECT COUNT(*) FROM core_product;"
count_psql = f'psql -U postgres -c "{count_sql}" estoque_teste'
subprocess.call(count_psql, shell=True)
```
## Rodar fora do notebook

```
python insert_with_create.py
python insert_with_bulk_create.py
python insert_with_psycopg2.py
python insert_with_subprocess.py
source insert_with_shell_script.sh
```



## Links

https://docs.python.org/3/howto/argparse.html

https://gist.github.com/rg3915/a42163d57a72c07c9780c97df3063a36

https://info.crunchydata.com/blog/fast-csv-and-json-ingestion-in-postgresql-with-copy

https://hakibenita.com/fast-load-data-python-postgresql

bulk_create

https://docs.djangoproject.com/en/2.2/ref/models/querysets/#bulk-create

Github: bulk_create

https://github.com/django/django/blob/master/django/db/models/query.py#L455

Github: Atomic transation

https://github.com/django/django/blob/master/django/db/models/query.py#L491

Database transactions

https://docs.djangoproject.com/en/3.0/topics/db/transactions/


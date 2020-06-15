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

## Porque não usar sqlite?

Faça um teste:

```
curl https://gist.githubusercontent.com/rg3915/b363f5c4a998f42901705b23ccf4b8e8/raw/5d0d1cc46d3a52bef6cd73d9d476140ad445be9e/boilerplatesimple.sh -o boilerplatesimple.sh
```

```
source boilerplatesimple.sh
```

Crie um models

```
class Product(models.Model):
    title = models.CharField('título', max_length=10)
    quantity = models.PositiveIntegerField('quantidade')

    class Meta:
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

    def __str__(self):
        return self.title
```

Abra shell

```
python manage.py shell_plus
```

E rode

```
title='Notebook i5 256Gb SSD 16Gb RAM'
print(len(title))

Product.objects.create(title=title)

Product.objects.all()
```

Crie um banco

```
sudo su - postgres
psql

 CREATE ROLE rg3915 ENCRYPTED PASSWORD '1234' LOGIN;

CREATE DATABASE mydb OWNER rg3915;

# Você pode se conectar no novo banco pra não precisar sair.
\c mydb

\q  # sair
```


Edite o settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'rg3915',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Abra o shell_plus novamente

e insira os dados novamente.



## Rodando os notebooks

```
python manage.py shell_plus --notebook
```

## Rodar fora do notebook

```
python insert_with_bulk_create.py
python insert_with_subprocess.py
time python insert_data_benchmark.py --rows 100000

chmod +x insert_with_shell_script.sh
./insert_with_shell_script.sh 1000000
```

### Observações

Se você inserir 14.000.605 registros com o método `insert_data_with_psycopg2_one_by_one` pode demorar `15680` segundos, ou seja, `4.35` horas.

## Testes num servidor

```
t2.large
vCPU: 2
Memória: 8 Gb
Volume: 20 Gb SSD
```

#### Instalar PostgreSQL

```
sudo apt update
sudo apt install -y postgresql-client postgresql curl wget git vim
```

#### Configurando alguns alias

```
alias h=history
alias pir='pip install -r requirements.txt'
alias sa='source .venv/bin/activate'
alias m='python $VIRTUAL_ENV/../manage.py'
```

Você pode colocar isso no `~/.bashrc`. Veja meu `.bash_profile` no meu [gist](https://gist.github.com/rg3915/0a0b1e514d11fdbc44f1).

#### Criando o banco de dados

Gerar uma senha qualquer.

```
openssl rand -base64 32
# ou
date | md5sum
```

```
sudo su - postgres
psql

 CREATE ROLE rg3915 ENCRYPTED PASSWORD '1234' LOGIN;

CREATE DATABASE estoque_teste OWNER rg3915;

# Você pode se conectar no novo banco pra não precisar sair.
\c estoque_teste

# Listar as tabelas
\dt

\q    # sair do banco
exit  # sair do postgres
```

Poderia usar os scripts

```
python create_database.py -d dbname -u username
# ou
python create_database_with_click.py -d dbname -u username
```


#### Instalar python3-venv

```
python3 -V

sudo apt install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
```


#### Clonar o projeto

```
git clone https://github.com/rg3915/fast-database.git
cd fast-database
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

Se der erros na instalação...

Erro:

```
...
Using legacy setup.py install for memory-profiler, since package 'wheel' is not installed.
...
```

O [memory-profiler](https://pypi.org/project/memory-profiler/) requer o [psutil](https://pypi.org/project/psutil/).

```
sudo apt install -y gcc python3-dev
pip3 install psutil
```

Por fim, faça novamente

```
pip install -r requirements.txt
```

E não esqueça de

```
python contrib/env_gen.py
python manage.py migrate
```

Agora vamos testar os scripts no servidor

Gerando os arquivos

```
mkdir ~/dados
python create_csv.py --rows 1000
```


Inserindo os dados

```
time python insert_data_benchmark.py --rows 1000

chmod +x insert_with_shell_script.sh
./insert_with_shell_script.sh 1000
```

Editar `pg_hba.conf`

sudo vim /etc/postgresql/10/main/pg_hba.conf

E mude `peer` para `trust` em

```
# Database administrative login by Unix domain socket
local   all             postgres                                peer
```
para

```
# Database administrative login by Unix domain socket
local   all             postgres                                trust
```

Restart

```
sudo systemctl reload postgresql
```


Editar `insert_with_shell_script.sh` e trocar o usuário

... mudar para

```
time psql -U postgres \
...
```

Agora vamos tentar rodar novamente

```
./insert_with_shell_script.sh 1000
```

**Atenção:** não façam isso em produção!

```
psql -U postgres -c "DELETE FROM core_product;" estoque_teste
```

3 brechas de segurança:

* Com o pg_hba.conf modificado você consegue rodar um script sem senha.
* NUNCA faça DELETE sem WHERE!
* Comandos direto no terminal são muito perigosos. Faça um `script*.sh` e modifique as permissões de acesso ao arquivo com `chmod`. Acesso de usuário, senha, etc.


## JSONField

[Django JSONField](https://docs.djangoproject.com/en/3.0/ref/contrib/postgres/fields/#jsonfield)

[PostgreSQL jsonb](https://www.postgresql.org/docs/current/functions-json.html)


```
# dropdb -U postgres dbteste
createdb -U postgres dbteste

sudo su - postgres
psql dbteste

CREATE TABLE product (id SERIAL PRIMARY KEY, title VARCHAR(100), quantity INTEGER, myjson JSONB);

INSERT INTO product (title, quantity) 
VALUES ('A', 1), 
('B', 2), 
('C', 3), 
('D', 4), 
('E', 5);

# psql -U postgres -c "COPY product (title, quantity) FROM '$HOME/dados/produtos_1000.csv' CSV HEADER;" dbteste

# DELETE FROM product;

SELECT * FROM product;

SELECT title, quantity, json_build_object('title', title, 'quantity', quantity) AS data FROM product;

SELECT id, json_build_object('title', title, 'quantity', quantity) AS data FROM product;

SELECT id::int, json_build_object('title', title, 'quantity', quantity) AS data FROM product;

CREATE TEMP TABLE temptable AS
  SELECT 1::int, '{"a":"b"}'::jsonb;

CREATE TEMP TABLE temptable AS
  SELECT id::int, json_build_object('title', title, 'quantity', quantity) AS data FROM product;

SELECT * FROM temptable LIMIT 5;

INSERT INTO product (id, myjson) (SELECT id, data FROM temptable);

SELECT * FROM product ORDER BY id DESC LIMIT 5;

UPDATE product t2
SET myjson = t1.data
FROM temptable t1
WHERE t2.id = t1.id;

SELECT * FROM product WHERE id > 997 LIMIT 6;

SELECT * FROM product WHERE id < 1010 ORDER BY id DESC LIMIT 15;
```

Descobri uma solução melhor para o jsonb:

```
UPDATE product
SET myjson = json_build_object('title', title, 'quantity', quantity);
```

com isso não precisa de tabela auxiliar.

## Links

[boilerplatesimple](https://gist.github.com/rg3915/b363f5c4a998f42901705b23ccf4b8e8)

[argparse](https://docs.python.org/3/howto/argparse.html)

[read csv](https://gist.github.com/rg3915/a42163d57a72c07c9780c97df3063a36)

[Fast CSV and JSON Ingestion in PostgreSQL with COPY](https://info.crunchydata.com/blog/fast-csv-and-json-ingestion-in-postgresql-with-copy)

[Fastest Way to Load Data Into PostgreSQL Using Python](https://hakibenita.com/fast-load-data-python-postgresql)

[bulk_create](https://docs.djangoproject.com/en/2.2/ref/models/querysets/#bulk-create)

[Github: bulk_create](https://github.com/django/django/blob/master/django/db/models/query.py#L455)

[Github: Atomic transation](https://github.com/django/django/blob/master/django/db/models/query.py#L491)

[Database transactions](https://docs.djangoproject.com/en/3.0/topics/db/transactions/)

[Juliano Atanazio postgresql_sql_basico.pdf](https://github.com/juliano777/pgsql_fs2w/blob/master/postgresql_sql_basico.pdf)

[Video: PostgreSQL, Django, Docker, Schemas e PLPython com Juliano Atanazio](https://www.youtube.com/watch?v=ABGbZYY4e3o)

[10 Ways to Generate a Random Password from the Linux Command Line](https://www.howtogeek.com/howto/30184/10-ways-to-generate-a-random-password-from-the-command-line/)

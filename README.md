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
    title = models.CharField('título', max_length=50)
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
title='notebook i3 SSD 8 Gb RAM'
print(len(title))

Product.objects.create(title=title)

Product.objects.all()
```

Crie um banco

```
sudo su - postgres
psql

 CREATE ROLE rg3915 ENCRYPTED PASSWORD '1234' LOGIN;

CREATE DATABASE estoque_teste OWNER rg3915;

# Você pode se conectar no novo banco pra não precisar sair.
\c estoque_teste

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
source insert_with_shell_script.sh
```



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


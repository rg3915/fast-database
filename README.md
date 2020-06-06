# fast-database

Exemplo de como inserir grande quantidade de dados da forma mais rápida num banco de dados PostgreSQL.

## This project was done with:

* Python 3.8.2
* Django 2.2.12

## How to run project?

* Clone this repository.
* Create virtualenv with Python 3.
* Active the virtualenv.
* Install dependences.
* Run the migrations.

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
* Django 2.2.12

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


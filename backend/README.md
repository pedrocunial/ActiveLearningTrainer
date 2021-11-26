# Backend

Esse serviço é responsável por toda a organização dos dados, comunicação com IBM Cloud e lógicas de escolha das amostras.

## Requerimentos

- Python 3.7+
- Pipenv
- Redis
- PostgreSQL

## Configurando o projeto

Se deseja executar o projeto localmente, algumas configurações são necessárias da primeira vez. Primeiramente, seu sistema deve possuir dois bancos de dados instalados: o [PostgreSQL](https://www.postgresql.org/) e o [Redis](https://redis.io/). Com as duas bases instaladas e configuradas, utilize o [Pipenv](https://github.com/pypa/pipenv) para configurar as dependências do projeto. Por último, faça as migrações necessárias do banco de dados utilizando o sistema de gerenciamento do Django.

### Base de Dados (PostgreSQL)

A base de dados utilizada no projeto é a PostgreSQL. Para isso é necessário que a sua máquina esteja com um servidor PostgreSQL rodando na porta 5432 (a porta padrão do serviço).

#### 1. Instale o servidor PostgreSQL (Ubuntu 18.04)
```sh
$ sudo apt install postgresql postgresql-contrib
```

#### 2. Crie a base de dados e o usuário
<pre>
$ sudo -u postgres psql
postgres=# CREATE DATABASE pfe_2018;
postgres=# CREATE USER admin WITH ENCRYPTED PASSWORD "password";
postgres=# GRANT ALL PRIVILEGES ON DATABASE pfe_2018 TO admin;
</pre>

### Base de Dados (Redis)

O Redis é uma base de dados em memória utilizada em conjunto com o Celery, apresentado abaixo. Usamos o Redis em sua configuração padrão

#### 1. Instale o Redis (Ubuntu 18.04)
```sh
$ sudo apt install redis-server
```

#### 2. Reinicie o serviço
```sh
$ sudo systemctl restart redis-server.service
```

### Dependências do Python

O projeto utiliza _Pipenv_ para gerencias suas dependências

#### 1. Instale o Pipenv
```sh
$ pip install --user pipenv
```

#### 2. Instale as dependências necessárias
```sh
$ pipenv install
```

#### 3. Acesse o ambiente virtual criado para o projeto
```sh
$ pipenv shell
```

#### ou rode comandos externamente
```sh
$ pipenv run <comando>
```

### Celery

O _Celery_ é a biblioteca utilizada para possibilitar o uso de _tasks_ assíncronas no nosso projeto. Ela utiliza o _redis_ como _backend_ para criar um servidor de filas seguindo um modelo de produtor-consumidor onde a _API_ dispara tarefas a serem feitas e a outra ponta consome estas tarefas (as realiza). Vale lembrar que o _celery_ depende do _backend_ do _redis_, então certifique-se de que tem um server do _redis_ rodando antes de iniciar o _celery_. Se o comando `$ pipenv install` rodou sem problemas, o Celery já está configurado.

### Migrações do Banco de Dados

Com os serviços configurados, a base de dados do projeto deve ser criada:
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

Toda vez que uma modificação for realizada no _schema_ da base de dados, os comandos acima devem ser executados.

## Rodando o projeto

A configuração do projeto já está pronta, agora devemos colocar o projeto para rodar.

#### 1. Defina as credencias do PostgreSQL a serem utilizadas para esta execução
```sh
$ export DB_USER=admin
$ export DB_PASS=password
$ export DB_NAME=pfe_2018
```

#### 2. Inicie o servidor Redis
```sh
$ redis-server
```

#### 3. Inicie o Celery
```sh
$ celery -A main worker -l info -E
```

#### 4. Inicie o servidor do projeto
```sh
$ python manage.py runserver
```

Se todos os passos foram seguidos corretamente, o servidor deve estar rodando localmente na porta 8000.

## Testes

Com todos os requisitos anteriores cumpridos, basta utilizar o comando `$ python manage.py test` para rodar todos os testes unitários do projeto. Os testes podem ser encontrados no arquivo `api/tests.py`

## Guia de estilo

Todas as modificações tem que estar de acordo com o [PEP 8](https://www.python.org/dev/peps/pep-0008/?)

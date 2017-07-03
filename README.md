## Projeto do grupo *Neoway 2*

#### Pip
*Faça isso antes de tudo*
`pip install -r requirements.txt`

#### PostgreSQL
* Install PostgreSQL 9.5
* `psql postgres`
  * `CREATE DATABASE novo_caminho;`
* `psql novo_caminho`
  * `CREATE USER caminho_user WITH PASSWORD 'abcdef';`
* `psql novo_caminho -c "GRANT ALL ON ALL TABLES IN SCHEMA public to caminho_user;"`
* `psql novo_caminho -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to caminho_user;"`
* `psql novo_caminho -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to caminho_user;"`
* `sudo nano /etc/postgresql/9.5/main/pg_hba.conf`
* Mudar o `peer` para `md5:`
```
# "local" is for Unix domain socket connections only
local   all             all                                     peer
```
* `sudo service postgresql restart`
* Pronto para fazer `python manage.py migrate`!

#### Get URLs from Search Engines
`get_urls(["jose dirceu","PT"], ["google","yahoo"], 3)` retorna um generator das URLs



#### Django
Versão 1.11.2

Para rodar o Django, entre na pasta do repositório(```novo-caminho/```) e use:

`python manage.py runserver`

#### MongoDB
Instalar Mongo 3.2.11, dai:

`$ mongo`

Dentro do Shell do MongoDB:

`> use novo_caminho`

`> db.createCollection("Article")`

Mongo configurado!!

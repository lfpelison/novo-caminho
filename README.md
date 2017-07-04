## Projeto do grupo *Neoway 2*

#### Pip
*Faça isso antes de tudo*
`pip install -r requirements.txt`

#### Heroku
* Instalar Heroku 6.12.0(IMPORTANTE SER ESSA VERSÃO)
* Depois de adicionar as changes que tu fez no branch(git add... git commit -m...) Faça:
* `git push heroku <seu-branch-aqui>:master -f`
* Esse comando irá apagar o que está no Heroku e colocar com o que está na sua branch. Se pushando do master:
* `git push heroku master -f`

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

#### Pip
`pip install -r requirements.txt`

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

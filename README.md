## Projeto do grupo *Neoway 2*

#### Get URLs from Search Engines
`get_urls(["jose dirceu","PT"], ["google","yahoo"], 3)` retorna um generator das URLs

#### Pip
`pip install -r requirements.txt`

#### Django
Versão 1.11.2

Para rodar o Django, entre na pasta do repositório(```novo-caminho/```) e use:

`python manage.py runserver`

#### MongoDB
Example:
```
#encoding: utf-8
from pymongo import MongoClient

client = MongoClient('localhost', 27017) # conecta com o mongo
db = client.novoCaminho                  # seleciona o banco de dados
news = db.news                           # seleciona a colecao

news.insert({'url':"www.cbf.com/Jose", 'content':'Jose dirceu ...'})
id = news.insert({'url':"www.cbf.com/Aecio"})
print news.find_one(id)
print news.find_one({'url':"www.cbf.com/Jose"})
```

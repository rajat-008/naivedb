# naivedb

NaiveDB is a easy to use all Python database, inspired by the [TinyDB project](https://github.com/msiemens/tinydb) and File Structures university course.

## Future enhancements
* Clean the code
* Wrtie tests and achieve 100% coverage
* Allow updates to database structure in a declarative manner( inspired by Django models and GCP Cloud Deployment Manager)
* Develop a simple CLI to interact with NaiveDB. As of now the only way to interact is trhough Python code.
* Allow addition and updation of Tables after DB creation.

## Decision log
* The format in which the table data is accepted, considering the ease to migrate to a delcarative format(and although it may seem verbose now, the declarative format will make the decision worth it).


## Getting started - Creating and using sample DB

### Creating Database
```python
from naivedb import NaiveDB

user={
    "name":"user",
    "fields":[
            "name",
            "id",
            "email"
    ],
    "primary_key":"email"
}

courses={
    "name":"courses",
    "fields":[
            "name",
            "id",
            "domain",
            "instructor"
    ],
    "primary_key":"id"
}

tables=[user, courses]

#create DB
NaiveDB.create_db(name = "my_db", loc = "/home/rajat/college", tables = tables)

```
### Instantiating DB and perform queries

#instantiate DB
db = NaiveDB(db_loc = "/home/rajat/college")

#insert in Table "user"
user1={"name":"user1","id":"2020", "email":"user1@naive.db"}
db.user.insert(user1)

#query the DB
db.user.search("user1@naive.db")
#output : {'name': 'user1', 'id': '2020', 'email': 'user1@naive.db'}

res = db.user.search("user2@naive.db")
#output : False
```

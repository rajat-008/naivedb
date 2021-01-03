# naivedb

NaiveDB is a easy to use all Python database, inspired by the [TinyDB project](https://github.com/msiemens/tinydb) and File Structures university course.

## Getting started - Creating and using sample DB
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

#instantiate DB
db = NaiveDB(db_loc = "/home/rajat/college")

#insert in Table "user"
user1={"name":"user1","id":"2020", "email":"user1@naive.db"}
db.user.insert(user1)

#query the DB
db.user.search("user1@naive.db")
```
Output:
```bash
{'name': 'user1', 'id': '2020', 'email': 'user1@naive.db'}
```
```python
res = db.user.search("user2@naive.db")
```
Output:
```bash
False

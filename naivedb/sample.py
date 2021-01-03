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
res=db.user.search("user1@naive.db")
{'name': 'user1', 'id': '2020', 'email': 'user1@naive.db'}

res = db.user.search("user2@naive.db")
from flask import Flask,render_template,request, redirect,url_for
from core import NaiveDB
app=Flask(__name__)
db=NaiveDB("naivedb/")


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/search",methods=["POST"])
def search():
    name=request.form.get("name")
    print(name)
    data=db.anime.search(name)
    print(data)
    return render_template("search.html",data=data)

@app.route("/update",methods=["POST"])
def update():
    data=request.form.to_dict(value,name)
    print(data)
    data=db.anime.update(data)
    print(data)
    return render_template("search.html",data=data)

    
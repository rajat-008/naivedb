from flask import Flask,render_template,request, redirect,url_for
from core import NaiveDB
app=Flask(__name__)
db=NaiveDB("naivedb/")

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/insert",methods=['GET','POST'])
def insert():
    if request.method=="GET":
        return render_template("insert.html")
    data=request.form.to_dict()
    db.anime.insert(data)
    return redirect(url_for("render_record",pkey=data["name"]))

@app.route("/record/<string:pkey>")
def render_record(pkey):
    data=db.anime.search(pkey)
    return render_template("display_record.html",data=data)

@app.route("/search",methods=["POST"])
def search():
    name=request.form.get("name")
    return redirect(url_for("render_record",pkey=name))


from flask import Flask,render_template,request, redirect,url_for
from naivedb.core import NaiveDB
app=Flask(__name__)
db=NaiveDB(".")

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
    if data==False:
        return "record not found",404
    return render_template("display_record.html",data=data)

@app.route("/fetch_all")
def fetch_all():
    records=db.anime.fetch_all()
    return render_template("display_all.html",records=records)


@app.route("/search",methods=["POST"])
def search():
    name=request.form.get("name")
    return redirect(url_for("render_record",pkey=name))

@app.route("/update/<string:pkey>",methods=['GET','POST'])
def update(pkey):
    if request.method=="GET":
        return render_template("update.html",pkey=pkey)
    data=request.form.to_dict()
    data["name"]=pkey
    db.anime.update(pkey,data)
    return redirect(url_for("render_record",pkey=pkey))


@app.route("/delete/<string:pkey>",methods=['GET',"POST"])
def delete(pkey):
    db.anime.delete(pkey)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
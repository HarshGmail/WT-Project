from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect, url_for
from datetime import datetime
from email.policy import default
from enum import unique
from re import A

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Khatabook_Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/",methods=["GET","POST"])
def loginpage():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if username=="Harsh" and password=="Harsh@123":
            return redirect(url_for("menu"))
    return render_template("login.html")

@app.route("/menu",methods=["GET","POST"])
def menu():
    if request.method=="POST":
        pass
    return render_template("menu.html")

if __name__=="__main__":
    app.run(debug=True)
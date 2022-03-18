from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect, url_for
from datetime import datetime
from email.policy import default
from enum import unique
from re import A


"""Configuration"""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Khatabook_Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

"Login Page"
@app.route("/",methods=["GET","POST"])
def loginpage():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        if username=="Harsh" and password=="Harsh@123":
            return redirect(url_for("menu"))
    return render_template("login.html")


""""".......................................DEALER SIDE........................................."""""
"""..............................................................................................."""
"Menu Page"
@app.route("/menu",methods=["GET","POST"])
def menu():
    if request.method=="POST":
        pass
    return render_template("menu.html")




"""Inventory"""
@app.route("/inventory",methods=["GET","POST"])
def inventory():
    if request.method=="POST":
        pass
    return render_template("inventory.html")

@app.route("/inventory_order",methods=["GET","POST"])
def inventory_order():
    if request.method=="POST":
        pass
    return render_template("inventory_order.html")




"""Staff"""
@app.route("/staff",methods=["GET","POST"])
def staff():
    if request.method=="POST":
        pass
    return render_template("staff.html")

@app.route("/staff_full_info",methods=["GET","POST"])
def staff_full_info():
    if request.method=="POST":
        pass
    return render_template("staff_full_info.html")

@app.route("/staff_modify_info",methods=["GET","POST"])
def staff_modify_info():
    if request.method=="POST":
        pass
    return render_template("staff_modify_info.html")




"""Salary payment"""
@app.route("/salary",methods=["GET","POST"])
def salary():
    if request.method=="POST":
        pass
    return render_template("salary.html")




"""Tax Management"""
@app.route("/tax_management",methods=["GET","POST"])
def tax_management():
    if request.method=="POST":
        pass
    return render_template("tax_management.html")




"""Customer Interface"""
@app.route("/customer_interface",methods=["GET","POST"])
def customer_interface():
    if request.method=="POST":
        pass
    return render_template("customer_interface.html")




"""Credit given and taken"""
@app.route("/credits",methods=["GET","POST"])
def credits():
    if request.method=="POST":
        pass
    return render_template("credits.html")

@app.route("/credit_info",methods=["GET","POST"])
def credit_info():
    if request.method=="POST":
        pass
    return render_template("credit_info.html")


"""""......................................CUSTOMER SIDE........................................"""""
"""..............................................................................................."""


if __name__=="__main__":
    app.run(debug=True)
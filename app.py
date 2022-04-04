from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request,redirect, url_for
from datetime import datetime
from email.policy import default
from enum import unique
from re import A
import cv2
from pyzbar import pyzbar
import sqlalchemy



"""........................................Configuration.........................................."""
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///My_Project_Database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

"""........................................Databases.............................................."""
db = SQLAlchemy(app)


class user_database(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    user_type=db.Column(db.String(10),nullable=False)
    user_password=db.Column(db.String(20),nullable=False)

class inventory_database(db.Model):
    item_id=db.Column(db.Integer,primary_key=True)
    item_name=db.Column(db.String(100),nullable=False)
    item_costprice=db.Column(db.Integer,nullable=False)
    item_selling_price=db.Column(db.Integer,nullable=False)
    item_available_number=db.Column(db.Integer,nullable=False)
    item_max_units=db.Column(db.Integer,nullable=False)

class suppliers_database(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    supplier_name=db.Column(db.String(30),nullable=False)
    supplier_credit=db.Column(db.Integer,nullable=False)


    
db.create_all()

".............Login Page.............."
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


"...............Menu Page................"
@app.route("/menu",methods=["GET","POST"])
def menu():
    if request.method=="POST":
        if request.form["inventory"]:
            return redirect(url_for("inventory"))
    return render_template("menu.html")




"""..............Inventory.................."""
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

@app.route("/inventory_add_item_page",methods=["GET","POST"])
def inventory_add_item():
    if request.method=="POST":
        itemid=request.form["itemid"]
        itemname=request.form["itemname"]
        costprice=request.form["costprice"]
        sellingprice=request.form["sellingprice"]
        availableunits=request.form["availableunits"]
        maxunits=request.form["maxunits"]
        rows=inventory_database.query.all()
        for row in rows:
            if row.itemid==itemid:
                return redirect(url_for("inventory_add_item_page"))
        row=inventory_database(item_id=itemid,item_name=itemname,item_costprice=costprice,item_selling_price=sellingprice,item_available_number=availableunits,item_max_units=maxunits)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("inventory"))
    return render_template("inventory_add_item_page.html")

@app.route("/inventory_modify_item",methods=["GET","POST"])
def inventory_modify_item():
    if request.method=="POST":
        pass
    return render_template("inventory_modify_item.html")


"""...............Staff................."""
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

@app.route("/staff_newemployee_addition",methods=["GET","POST"])
def staff_newemployee_addition():
    if request.method=="POST":
        pass
    return render_template("staff_newemployee_addition.html")

@app.route("/staff_employee_modification",methods=["GET","POST"])
def staff_employee_modification():
    if request.method=="POST":
        pass
    return render_template("staff_employee_modification.html")




"""............Salary payment..........."""
@app.route("/salary",methods=["GET","POST"])
def salary():
    if request.method=="POST":
        pass
    return render_template("salary.html")




"""..............Tax Management.................."""
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





@app.route("/billinginterface",methods=["GET","POST"])
def billinginterface():
    if request.method=="POST":
        pass
    return render_template("billinginterface.html")





"""""......................................CUSTOMER SIDE........................................"""""
"""..............................................................................................."""


if __name__=="__main__":
    app.run(debug=True)
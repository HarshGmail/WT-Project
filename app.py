import email
from datetime import datetime
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
    user_name=db.Column(db.String(10),nullable=False)
    user_password=db.Column(db.String(20),nullable=False)
    user_type=db.Column(db.String(20),nullable=False)
    user_phone_number=db.Column(db.String(15),nullable=False)
    user_address=db.Column(db.String(200),nullable=False)


class inventory_database(db.Model):
    item_id=db.Column(db.Integer,primary_key=True)
    item_name=db.Column(db.String(100),nullable=False)
    item_costprice=db.Column(db.Integer,nullable=False)
    item_selling_price=db.Column(db.Integer,nullable=False)
    item_available_number=db.Column(db.Integer,nullable=False)
    item_max_units=db.Column(db.Integer,nullable=False)

class suppliers_database(db.Model):
    supplier_id=db.Column(db.Integer,primary_key=True)
    supplier_name=db.Column(db.String(30),nullable=False)
    supplier_supply_items=db.Column(db.Integer,nullable=False)

class credit_database(db.Model):
    supplier_id=db.Column(db.Integer,primary_key=True)
    supplier_credit_given_date=db.Column(db.DateTime,default=datetime.utcnow)
    supplier_name=db.Column(db.Integer,nullable=False)
    supplier_supplied_amount=db.Column(db.Integer,nullable=False)
    supplier_credit_limit=db.Column(db.Integer,nullable=False)

class employee_database(db.Model):
    employee_id=db.Column(db.Integer,primary_key=True)
    employee_name=db.Column(db.String(30),nullable=False)
    employee_basic=db.Column(db.Integer,nullable=False)
    employee_bloodgroup=db.Column(db.String(5),nullable=False)
    employee_designation=db.Column(db.String(25),nullable=False)
    employee_address=db.Column(db.String(200),nullable=False)
    employee_aadharno=db.Column(db.String(12),nullable=False)
    employee_phonenumber=db.Column(db.String(10),nullable=False)
    employee_dob=db.Column(db.String(10),nullable=False)
    employee_fathername=db.Column(db.String(20),nullable=False)
    employee_mothername=db.Column(db.String(20),nullable=False)
    employee_emailid=db.Column(db.String(40),nullable=False)
    employee_sex=db.Column(db.String(11),nullable=False)
    employee_bankaccountno=db.Column(db.String(18),nullable=False)
    employee_bankname=db.Column(db.String(30),nullable=False)
    employee_bankifsc=db.Column(db.String(11),nullable=False)

class store_database(db.Model):
    store_id=db.Column(db.String(10),primary_key=True)
    store_name=db.Column(db.String(50),nullable=False)
    store_address=db.Column(db.String(200),nullable=False)
    store_phone_number=db.Column(db.String(13),nullable=False)
    store_type=db.Column(db.String(20),nullable=False)

class stores_orders_database(db.Model):
    store_order_id=db.Column(db.String(12),primary_key=True)
    store_order_details=db.Column(db.String(1000),nullable=False)
    store_order_total=db.Column(db.Integer,nullable=False)
    store_id=db.Column(db.String(12),nullable=False)
    store_order_profit_total=db.Column(db.Integer,nullable=False)

class temp_database(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    id=db.Column(db.String(12),nullable=False)
    name=db.Column(db.String(30),nullable=False)
    qty=db.Column(db.Integer,nullable=False)
    sp=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Integer,nullable=False)

class orders_database(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    store_id=db.Column(db.Integer,nullable=False)
    order_items_id=db.Column(db.String(1500),nullable=False)
    customer_id=db.Column(db.Integer,nullable=False)
    order_total=db.Column(db.Integer,nullable=False)
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

@app.route("/signup",methods=["GET","POST"])
def signup():
    return render_template("signup.html")


""""".......................................DEALER SIDE........................................."""""
"""..............................................................................................."""


"...............Menu Page................"
@app.route("/menu",methods=["GET","POST"])
def menu():
    return render_template("menu.html")




"""..............Inventory.................."""
@app.route("/inventory",methods=["GET","POST"])
def inventory():
    allrows=inventory_database.query.all()
    return render_template("inventory.html",idb=allrows)

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
            if row.item_id==itemid:
                return redirect(url_for("inventory_add_item_page"))
        row=inventory_database(item_id=itemid,item_name=itemname,item_costprice=costprice,item_selling_price=sellingprice,item_available_number=availableunits,item_max_units=maxunits)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("inventory"))
    return render_template("inventory_add_item_page.html")

@app.route("/inventory_modify_item",methods=["GET","POST"])
def inventory_modify_item():
    if request.method=="POST":
        oldid=request.form["olditemid"]
        itemid=request.form["itemid"]
        itemname=request.form["itemname"]
        costprice=request.form["costprice"]
        sellingprice=request.form["sellingprice"]
        availableunits=request.form["availableunits"]
        maxunits=request.form["maxunits"]
        row=inventory_database.query.filter_by(item_id=oldid).first()
        row.item_id=itemid
        row.item_name=itemname
        row.item_costprice=costprice
        row.item_selling_price=sellingprice
        row.item_available_number=availableunits
        row.item_maximum_units=maxunits
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("inventory"))
    return render_template("inventory_modify_item.html")

@app.route("/inventory_updation",methods=["GET","POST"])
def inventory_updation():
    if request.method=="POST":
        itemid=request.form["itemid"]
        costprice=request.form["costprice"]
        sellingprice=request.form["sellingprice"]
        availableunits=request.form["availableunits"]
        maxunits=request.form["maxunits"]
        row=inventory_database.query.filter_by(item_id=itemid).first()
        row.item_costprice=costprice
        row.item_selling_price=sellingprice
        row.item_available_number=availableunits
        row.item_maximum_units=maxunits
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("inventory"))
    return render_template("inventory_updation.html")



"""...............Staff................."""
@app.route("/staff",methods=["GET","POST"])
def staff():
    allrows=employee_database.query.all()
    return render_template("staff.html",edb=allrows)

@app.route("/staff_full_info",methods=["GET","POST"])
def staff_full_info():
    if request.method=="POST":
        pass
    return render_template("staff_full_info.html")

@app.route("/staff_newemployee_addition",methods=["GET","POST"])
def staff_newemployee_addition():
    if request.method=="POST":
        emp_id=request.form["employeeid"]
        ename=request.form["employeename"]
        basic=request.form["basic"]
        bgrp=request.form["bloodgroup"]
        desg=request.form["designation"]
        address=request.form["address"]
        aadno=request.form["aadharno"]
        phoneno=request.form["phoneno"]
        dob=request.form["dob"]
        fatname=request.form["fatname"]
        motname=request.form["motname"]
        emailid=request.form["emailid"]
        sex=request.form["sex"]
        bacctno=request.form["bankaccountno"]
        bname=request.form["bankname"]
        bifsc=request.form["bankifsc"]
        rows=employee_database.query.all()
        for row in rows:
            if row.employee_id==emp_id:
                return render_template("staff_newemployee_addition")
        row=employee_database(employee_id=emp_id,employee_name=ename,employee_basic=basic,
        employee_bloodgroup=bgrp,employee_designation=desg,employee_address=address,
        employee_aadharno=aadno,employee_phonenumber=phoneno,employee_dob=dob,
        employee_fathername=fatname,employee_mothername=motname,employee_emailid=emailid,
        employee_sex=sex,employee_bankaccountno=bacctno,employee_bankname=bname,employee_bankifsc=bifsc)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("staff"))
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
    sod=stores_orders_database.query.all()
    return render_template("tax_management.html",sod=sod)




"""Customer Interface"""
@app.route("/customer_interface",methods=["GET","POST"])
def customer_interface():
    allrows=inventory_database.query.all()
    return render_template("customer_interface.html",idb=allrows)




"""Credit given and taken"""
@app.route("/credits",methods=["GET","POST"])
def credits():
    cdb=credit_database.query.all()
    return render_template("credits.html",cdb=cdb)

@app.route("/credit_info",methods=["GET","POST"])
def credit_info():
    if request.method=="POST":
        pass
    return render_template("credit_info.html")

@app.route("/supplieraddition",methods=["GET","POST"])
def supplieraddition():
    if request.method=="POST":
        supplier_id=request.form["supplierid"]
        supplier_name=request.form["suppliername"]
        supplier_items=request.form["supplieritems"]
        row=suppliers_database(supplier_id=supplier_id,supplier_name=supplier_name,supplier_supply_items=supplier_items)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("credits"))
    return render_template("supplieraddition.html")

@app.route("/newcredittransaction",methods=["GET","POST"])
def newcredittransaction():
    if request.method=="POST":
        supplier_id=request.form["supplierid"]
        amount=request.form["amount"]
        days=request.form["creditdays"]
        sdb=suppliers_database.query.all()
        name=""
        for row in sdb:
            if int(row.supplier_id)==int(supplier_id):
                name=row.supplier_name
        row=credit_database.query.filter_by(supplier_id=supplier_id).first()
        if row:
            row.supplier_supplied_amount=int(row.supplier_supplied_amount)+int(amount)
            row.supplier_credit_limit=int(row.supplier_credit_limit)+int(days)
        else:
            row=credit_database(supplier_id=supplier_id,supplier_name=name,supplier_supplied_amount=amount,supplier_credit_limit=days)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("credits"))
    return render_template("newcredittransaction.html")




"""................Billing Interface..................."""
@app.route("/billinginterface",methods=["GET","POST"])
def billinginterface():
    if request.method=="POST":
        item_id=int(request.form["itemid"])
        qty=request.form["qty"]
        if item_id==None or qty ==None:
            return render_template("billinginterface.html")
        idb=inventory_database.query.all()
        sp=0
        name=""
        row=None
        for row in idb:
            if row.item_id==item_id:
                sp=row.item_selling_price
                name=row.item_name
                row.item_available_number-=int(qty)
                break
        db.session.add(row)
        db.session.commit()
        price=int(sp)*int(qty)
        tdb=temp_database.query.all()
        ns=0
        for _ in tdb:
            ns=_.sno
        sno=ns+1
        row=temp_database(sno=sno,id=item_id,name=name,qty=qty,sp=sp,price=price)
        db.session.add(row)
        db.session.commit()
    if request.method=="POST1":
        print("d")
        return redirect(url_for("billpreview"))
    tdb=temp_database.query.all()
    return render_template("billinginterface.html",tdb=tdb)

@app.route("/billpreview",methods=["GET","POST"])
def billpreview():
    if request.method=="POST":
        tdb=temp_database.query.all()
        idb=inventory_database.query.all()
        ttdb=tdb
        for row in tdb:
            db.session.delete(row)
            db.session.commit()
        s=""
        sod=stores_orders_database.query.all()
        for row in sod:
            s=row.store_order_id
        if s=="":
            k=1 
        else:
            k=int(s)+1
        p=""
        total=0
        profit=0
        for row in ttdb:
            p=p+f"{row.id}-{row.name}({row.qty})({row.price}),"
            total+=int(row.price)
            for r in idb:
                if int(r.item_id)==int(row.id):
                    profit+=(r.item_selling_price-r.item_costprice)*row.qty
        row=stores_orders_database(store_order_id=k+1,store_order_details=p,store_order_total=total,store_id=1,store_order_profit_total=profit)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("billinginterface"))
    tdb=temp_database.query.all()
    gtotal=0
    for row in tdb:
        gtotal+=int(row.price)
    return render_template("billpreview.html",tdb=tdb,gtotal=gtotal)




"""""......................................CUSTOMER SIDE........................................"""""
"""..............................................................................................."""
@app.route("/customerhomepage",methods=["GET","POST"])
def customerhomepage():
    return render_template("customerhomepage.html")


@app.route("/customerstorepage",methods=["GET","POST"])
def customerstorepage():
    return render_template("customerstorepage.html")


@app.route("/customerorderconfirmationpage",methods=["GET","POST"])
def customerorderconfirmationpage():
    return render_template("customerorderconfirmationpage.html")


if __name__=="__main__":
    app.run(debug=True)
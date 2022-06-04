from contextlib import redirect_stdout
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
    user_email_id=db.Column(db.String(200),nullable=False)

class inventory_database(db.Model):
    item_id=db.Column(db.Integer,primary_key=True)
    store_id=db.Column(db.Integer,nullable=False)
    item_name=db.Column(db.String(100),nullable=False)
    item_costprice=db.Column(db.Integer,nullable=False)
    item_selling_price=db.Column(db.Integer,nullable=False)
    item_available_number=db.Column(db.Integer,nullable=False)
    item_max_units=db.Column(db.Integer,nullable=False)

class suppliers_database(db.Model):
    supplier_id=db.Column(db.Integer,primary_key=True)
    store_id=db.Column(db.Integer,nullable=False)
    supplier_name=db.Column(db.String(30),nullable=False)
    supplier_supply_items=db.Column(db.Integer,nullable=False)

class credit_database(db.Model):
    supplier_id=db.Column(db.Integer,primary_key=True)
    store_id=db.Column(db.Integer,nullable=False)
    supplier_credit_given_date=db.Column(db.DateTime,default=datetime.utcnow)
    supplier_name=db.Column(db.Integer,nullable=False)
    supplier_supplied_amount=db.Column(db.Integer,nullable=False)
    supplier_credit_limit=db.Column(db.Integer,nullable=False)

class employee_database(db.Model):
    employee_id=db.Column(db.Integer,primary_key=True)
    store_id=db.Column(db.Integer,nullable=False)
    employee_name=db.Column(db.String(30),nullable=False)
    employee_basic=db.Column(db.Integer,nullable=False)
    employee_bloodgroup=db.Column(db.String(5),nullable=False)
    employee_address=db.Column(db.String(200),nullable=False)
    employee_aadharno=db.Column(db.String(12),nullable=False)
    employee_phonenumber=db.Column(db.String(10),nullable=False)
    employee_dob=db.Column(db.String(10),nullable=False)
    employee_fathername=db.Column(db.String(20),nullable=False)
    employee_mothername=db.Column(db.String(20),nullable=False)
    employee_emailid=db.Column(db.String(40),nullable=False)
    employee_sex=db.Column(db.String(11),nullable=False)
    employee_department=db.Column(db.String(40),nullable=False)
    employee_bankaccountno=db.Column(db.String(18),nullable=False)
    employee_bankname=db.Column(db.String(30),nullable=False)
    employee_bankifsc=db.Column(db.String(11),nullable=False)

class store_database(db.Model):
    store_id=db.Column(db.String(10),primary_key=True)
    store_owner_name=db.Column(db.String(50),nullable=False)
    store_uid=db.Column(db.String(40),nullable=False)
    store_name=db.Column(db.String(50),nullable=False)
    store_address=db.Column(db.String(200),nullable=False)
    store_phone_number=db.Column(db.String(13),nullable=False)
    store_email_id=db.Column(db.String(60),nullable=False)
    store_type=db.Column(db.String(20),nullable=False)

class stores_orders_database(db.Model):
    store_order_id=db.Column(db.String(12),primary_key=True)
    store_order_details=db.Column(db.String(1000),nullable=False)
    store_order_total=db.Column(db.Integer,nullable=False)
    store_id=db.Column(db.String(12),nullable=False)
    store_order_profit_total=db.Column(db.Integer,nullable=False)

class temp_database(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    store_id=db.Column(db.Integer,nullable=False)
    id=db.Column(db.String(12),nullable=False)
    name=db.Column(db.String(30),nullable=False)
    qty=db.Column(db.Integer,nullable=False)
    sp=db.Column(db.Integer,nullable=False)
    price=db.Column(db.Integer,nullable=False)

class orders_database(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    store_id=db.Column(db.Integer,nullable=False)
    store_order_details=db.Column(db.String(1500),nullable=False)
    customer_id=db.Column(db.Integer,nullable=False)
    pickup=db.Column(db.String(25),nullable=False)
    store_order_profit_total=db.Column(db.Integer,nullable=False)
    store_order_total=db.Column(db.Integer,nullable=False)

db.create_all()
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""







"...........................................Login Page..............................................."
@app.route("/",methods=["GET","POST"]) 
def loginpage():
    if request.method=="POST":
        allrows=user_database.query.all()
        username=request.form["username"]
        password=request.form["password"]
        if username=="Harsh" and password=="Harsh@123":
            return redirect(url_for("menu",username=username))
        elif username=='' and password=='':
            return redirect(url_for("signup"))
        for row in allrows:
            if row.user_name==username and row.user_password==password:
                if row.user_type=='admin':
                    sid=findstoreid(username)
                    # f=f"/menu/{sid}/{username}"
                    return redirect(url_for("menu",username=username,sid=sid))
                elif row.user_type=='staff':
                    arows=employee_database.query.all()
                    for rw in arows:
                        if row.user_phonenumber==rw.employee_phonenumber:
                            if row.employee_department=='inventory':
                                return redirect(url_for("staffinventory",username=username))
                            elif row.employee_department=='billing':
                                return redirect(url_for("staffbilling",username=username))
                            elif row.employee_department=="orders":
                                return redirect(url_for("stafforder",username=username))
                else:
                    return redirect(url_for("cutomerhomepage",username))
    return render_template("login.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]
        typeofuser=request.form["typeofuser"].lower()
        phonenumber=request.form["phonenumber"]
        address=request.form["address"]
        emailid=request.form["emailid"]
        all=user_database.query.all()
        sno=0
        for row in all:
            sno=int(row.sno)
        sno+=1
        row=user_database(sno=sno,user_name=username,user_password=password,user_type=typeofuser,
                            user_phone_number=phonenumber,user_address=address,user_email_id=emailid)
        db.session.add(row)
        db.session.commit()
        if typeofuser=='admin':
            return redirect(url_for("signup_store",username=username))
        elif typeofuser=='staff':
            allrows=employee_database.query.all()
            for row in allrows:
                if phonenumber==row.employee_phonenumber:
                    if row.employee_department=='inventory':
                        store_id=findstoreidstaff(username)
                        store_id=int(store_id)
                        row=store_database.query.filter_by(store_id=store_id).first()
                        storename=row.store_name
                        return redirect(url_for("staffinventory",username=username,storename=storename))
                    elif row.employee_department=='billing':
                        return redirect(url_for("staffbilling",username=username))
                    elif row.employee_department=="orders":
                        return redirect(url_for("stafforder",username=username))
        else:
            return redirect(url_for("customerhomepage",username=username))
    return render_template("signup.html")

@app.route("/profile",methods=["GET","POST"])
def profile():
    return render_template("profile.html")

@app.route("/profilemodify",methods=["GET,POST"])
def profilemodify():
    return render_template("profilemodify.html")

@app.route("/signup_store/<username>",methods=["GET","POST"])
def signup_store(username):
    store_owner_name=username
    if request.method=="POST":
        storename=request.form["storename"]
        uid=request.form["uid"]
        typeofstore=request.form["typeofstore"]
        phonenumber=request.form["phonenumber"]
        address=request.form["address"]
        emailid=request.form["emailid"]
        allrows=store_database.query.all()
        sno=0
        for row in allrows:
            sno=int(row.store_id)
        if sno==0:
            sno=1
        else:
            sno+=1
        row=store_database(store_id=sno,store_uid=uid,store_owner_name=store_owner_name,store_name=storename,store_email_id=emailid,
                            store_phone_number=phonenumber,store_address=address,store_type=typeofstore)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("inventory",username=username,storename=storename))
    return render_template("signup_store.html",username=username)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""







""""".......................................DEALER SIDE........................................."""""
def findstoreid(username):
    alr=store_database.query.all()
    store_id=1
    for row in alr:
        if row.store_owner_name==username:
            store_id=row.store_id
            break
    return int(store_id)

def findstoreidstaff(username):
    alr=employee_database.query.all()
    store_id=1
    for row in alr:
        if row.employee_name==username:
            store_id=row.store_id
            break
    return int(store_id)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""






"""............................................Menu Page............................................"""
@app.route("/menu/<sid>/<username>",methods=["GET","POST"])
def menu(sid,username):
    store_id=int(sid)
    return render_template("menu.html",sid=store_id,username=username)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""










"""..........................................Inventory.............................................."""
@app.route("/inventory/<username>",methods=["GET","POST"])
def inventory(username):
    allrows=inventory_database.query.all()
    store_id=findstoreid(username)
    store_id=int(store_id)
    row=store_database.query.filter_by(store_id=store_id).first()
    storename=row.store_name
    return render_template("inventory.html",idb=allrows,sid=store_id,username=username,storename=storename)

@app.route("/inventory_order/<username>",methods=["GET","POST"])
def inventory_order():
    if request.method=="POST":
        pass
    return render_template("inventory_order.html")

@app.route("/inventory_add_item_page/<sid>/<username>",methods=["GET","POST"])
def inventory_add_item(sid,username):
    if request.method=="POST":
        itemid=request.form["itemid"]
        itemname=request.form["itemname"]
        costprice=request.form["costprice"]
        sellingprice=request.form["sellingprice"]
        availableunits=request.form["availableunits"]
        maxunits=request.form["maxunits"]
        store_id=sid
        rows=inventory_database.query.all()
        for row in rows:
            if row.item_id==itemid:
                return redirect(url_for("inventory_add_item_page",sid=sid,username=username))
        row=inventory_database(item_id=itemid,item_name=itemname,item_costprice=costprice,
                                item_selling_price=sellingprice,item_available_number=availableunits,
                                item_max_units=maxunits,store_id=store_id)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("inventory",username=username))
    return render_template("inventory_add_item_page.html",username=username)

@app.route("/inventory_modify_item/<sid>/<username>",methods=["GET","POST"])
def inventory_modify_item(sid,username):
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
        row.store_id=int(sid)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("inventory",username=username))
    return render_template("inventory_modify_item.html",username=username)

@app.route("/inventory_updation/<sid>/<username>",methods=["GET","POST"])
def inventory_updation(sid,username):
    if request.method=="POST":
        itemid=request.form["itemid"]
        costprice=request.form["costprice"]
        sellingprice=request.form["sellingprice"]
        availableunits=request.form["availableunits"]
        maxunits=request.form["maxunits"]
        row=inventory_database.query.filter_by(item_id=itemid).first()
        row.item_costprice=costprice
        row.store_id=int(sid)
        row.item_selling_price=sellingprice
        row.item_available_number=availableunits
        row.item_maximum_units=maxunits
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("inventory",username=username))
    return render_template("inventory_updation.html")
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""

















"""...........................................Staff................................................."""
@app.route("/staff/<username>",methods=["GET","POST"])
def staff(username):
    store_id=int(findstoreid(username))
    allrows=employee_database.query.all()
    return render_template("staff.html",edb=allrows,sid=store_id,username=username)

@app.route("/staff_full_info/<username>",methods=["GET","POST"])
def staff_full_info():
    return render_template("staff_full_info.html")

@app.route("/staff_newemployee_addition/<username>",methods=["GET","POST"])
def staff_newemployee_addition(username):
    if request.method=="POST":
        emp_id=request.form["employeeid"]
        ename=request.form["employeename"]
        basic=request.form["basic"]
        bgrp=request.form["bloodgroup"]
        dept=request.form["department"]
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
        sid=int(findstoreid(username))
        rows=employee_database.query.all()
        for row in rows:
            if row.employee_id==emp_id:
                return render_template("staff_newemployee_addition",username=username)
        row=employee_database(employee_id=emp_id,store_id=sid,employee_name=ename,employee_basic=basic,
        employee_bloodgroup=bgrp,employee_department=dept,employee_address=address,
        employee_aadharno=aadno,employee_phonenumber=phoneno,employee_dob=dob,
        employee_fathername=fatname,employee_mothername=motname,employee_emailid=emailid,
        employee_sex=sex,employee_bankaccountno=bacctno,employee_bankname=bname,employee_bankifsc=bifsc)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("staff",username=username))
    return render_template("staff_newemployee_addition.html")

@app.route("/staff_employee_modification/<username>",methods=["GET","POST"])
def staff_employee_modification():
    return render_template("staff_employee_modification.html")

@app.route("/staffbilling/<username>",methods=["GET","POST"])
def staffbilling(username):
    if request.method=="POST":
        sid=int(findstoreidstaff(username))
        item_id=int(request.form["itemid"])
        qty=request.form["qty"]
        if item_id==None or qty ==None:
            return render_template("staffbilling.html",username=username)
        idb=inventory_database.query.all()
        sp=0
        name=""
        row=None
        for row in idb:
            if row.item_id==item_id and row.store_id==sid:
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
        row=temp_database(sno=sno,id=item_id,name=name,qty=qty,sp=sp,price=price,store_id=sid)
        db.session.add(row)
        db.session.commit()
    if request.method=="POST1":
        return redirect(url_for("staffbillpreview",username=username))
    tdb=temp_database.query.all()
    sid=findstoreid(username)
    return render_template("staffbilling.html",tdb=tdb,username=username)

@app.route("/staffinventory/<username>",methods=["GET","POST"])
def staffinventory(username):
    sid=findstoreidstaff(username)
    idb=inventory_database.query.all()
    return render_template("staffinventory.html",sid=sid,idb=idb,username=username)

@app.route("/stafforder/<username>",methods=["GET","POST"])
def stafforder(username):
    return render_template("stafforder.html")

@app.route("/staffbillpreview/<username>",methods=["GET","POST"])
def staffbillpreview(username):
    if request.method=="POST":
        tdb=temp_database.query.all()
        idb=inventory_database.query.all()
        sid=findstoreid(username)
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
        row=stores_orders_database(store_order_id=k+1,store_order_details=p,store_order_total=total,store_id=sid,store_order_profit_total=profit)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("staffbilling",username=username))
    tdb=temp_database.query.all()
    gtotal=0
    sid=findstoreid(username)
    for row in tdb:
        gtotal+=int(row.price)
    return render_template("staffbillpreview.html",tdb=tdb,gtotal=gtotal,sid=sid,username=username)

@app.route("/staffinventoryaddnewitem/<sid>/<username>",methods=["GET","POST"])
def staffinventoryaddnewitem(username,sid):
    if request.method=="POST":
        itemid=request.form["itemid"]
        itemname=request.form["itemname"]
        costprice=request.form["costprice"]
        sellingprice=request.form["sellingprice"]
        availableunits=request.form["availableunits"]
        maxunits=request.form["maxunits"]
        store_id=sid
        rows=inventory_database.query.all()
        for row in rows:
            if row.item_id==itemid:
                return redirect(url_for("staffinventoryaddnewitem",sid=sid,username=username))
        row=inventory_database(item_id=itemid,item_name=itemname,item_costprice=costprice,
                                item_selling_price=sellingprice,item_available_number=availableunits,
                                item_max_units=maxunits,store_id=store_id)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("staffinventory",username=username))
    return render_template("staffinventoryaddnewitem.html",username=username,sid=sid)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""







""".........................................Salary payment........................................."""
@app.route("/salary/<username>",methods=["GET","POST"])
def salary():
    if request.method=="POST":
        pass
    return render_template("salary.html")
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""









""".........................................Tax Management.........................................."""
@app.route("/tax_management/<username>",methods=["GET","POST"])
def tax_management(username):
    store_id=findstoreid(username)
    sod=stores_orders_database.query.all()
    return render_template("tax_management.html",sod=sod,username=username,sid=store_id)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""










""".....................................Customer Interface.........................................."""
@app.route("/customer_interface/<username>",methods=["GET","POST"])
def customer_interface(username):
    allrows=inventory_database.query.all()
    store_id=int(findstoreid(username))
    return render_template("customer_interface.html",idb=allrows,sid=store_id,username=username)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""









"""....................................Credit given and taken......................................."""
@app.route("/credits/<username>",methods=["GET","POST"])
def credits(username):
    cdb=credit_database.query.all()
    sid=findstoreid(username)
    return render_template("credits.html",cdb=cdb,username=username,sid=sid)

@app.route("/credit_info/<username>",methods=["GET","POST"])
def credit_info():
    return render_template("credit_info.html")

@app.route("/supplieraddition/<username>",methods=["GET","POST"])
def supplieraddition(username):
    store_id=findstoreid(username)
    if request.method=="POST":
        supplier_id=request.form["supplierid"]
        supplier_name=request.form["suppliername"]
        supplier_items=request.form["supplieritems"]
        row=suppliers_database(store_id=store_id,supplier_id=supplier_id,supplier_name=supplier_name,supplier_supply_items=supplier_items)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("credits",username=username))
    return render_template("supplieraddition.html",username=username,sid=store_id)

@app.route("/newcredittransaction/<username>",methods=["GET","POST"])
def newcredittransaction(username):
    sid=findstoreid(username)
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
            row=credit_database(store_id=sid,supplier_id=supplier_id,supplier_name=name,supplier_supplied_amount=amount,supplier_credit_limit=days)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("credits",username=username))
    return render_template("newcredittransaction.html",username=username,sid=sid)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""











"""...................................Billing Interface............................................"""
@app.route("/billinginterface/<username>",methods=["GET","POST"])
def billinginterface(username):
    if request.method=="POST":
        sid=findstoreid(username)
        item_id=int(request.form["itemid"])
        qty=request.form["qty"]
        if item_id==None or qty ==None:
            return render_template("billinginterface.html",username=username)
        idb=inventory_database.query.all()
        sp=0
        name=""
        row=None
        for row in idb:
            if row.item_id==item_id and row.store_id==sid:
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
        row=temp_database(sno=sno,id=item_id,name=name,qty=qty,sp=sp,price=price,store_id=sid)
        db.session.add(row)
        db.session.commit()
    if request.method=="POST1":
        return redirect(url_for("billpreview",username=username))
    tdb=temp_database.query.all()
    sid=findstoreid(username)
    return render_template("billinginterface.html",tdb=tdb,username=username,sid=sid)

@app.route("/billpreview/<username>",methods=["GET","POST"])
def billpreview(username):
    if request.method=="POST":
        tdb=temp_database.query.all()
        idb=inventory_database.query.all()
        sid=findstoreid(username)
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
        row=stores_orders_database(store_order_id=k+1,store_order_details=p,store_order_total=total,store_id=sid,store_order_profit_total=profit)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("billinginterface",username=username))
    tdb=temp_database.query.all()
    gtotal=0
    sid=findstoreid(username)
    for row in tdb:
        gtotal+=int(row.price)
    return render_template("billpreview.html",tdb=tdb,gtotal=gtotal,sid=sid,username=username)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""













"""""......................................CUSTOMER SIDE........................................"""""
"""..............................................................................................."""

def findstorename(sid):
    allrows=store_database.query.all()
    for row in allrows:
        if sid==row.store_id:
            return row.store_name

@app.route("/customerhomepage/<username>",methods=["GET","POST"])
def customerhomepage(username):
    if request.method=='POST':
        storename=request.form["storename"]
        sdb=store_database.query.all()
        store_id=0
        for row in sdb:
            if row.store_name==storename:
                store_id=row.store_id
                return redirect(url_for("customerstorepage",username=username,sid=store_id,storename=storename))
    return render_template("customerhomepage.html",username=username)


@app.route("/customerstorepage/<username>/<sid>",methods=["GET","POST"])
def customerstorepage(username,sid):
    storename=findstorename(sid)
    idb=inventory_database.query.all()
    return render_template("customerstorepage.html",username=username,sid=int(sid),storename=storename,idb=idb)

@app.route("/customerorderinfo/<username>/<itemid>/<sid>",methods=["GET","POST"])
def customerorderinfo(username,itemid,sid):
    if request.method=="POST":
        item_id=int(itemid)
        storename=findstorename(sid)
        qty=request.form["qty"]
        idb=inventory_database.query.all()
        sp=0
        name=""
        row=None
        for row in idb:
            if int(row.item_id)==item_id and int(row.store_id)==int(sid):
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
        row=temp_database(sno=sno,id=item_id,name=name,qty=qty,sp=sp,price=price,store_id=sid)
        db.session.add(row)
        db.session.commit()
        return redirect(url_for("customerstorepage",username=username,sid=sid))
    idb=inventory_database.query.all()
    for row in idb:
        if row.item_id==int(itemid):
            return render_template("customerorderinfo.html",username=username,itemid=itemid,sid=sid,idb=idb,row=row)        
    return render_template("customerorderinfo.html",username=username,itemid=itemid,sid=sid,idb=idb)

@app.route("/customerorderconfirmationpage/<username>",methods=["GET","POST"])
def customerorderconfirmationpage(username):
    odb=orders_database.query.all()
    return render_template("customerorderconfirmationpage.html",username=username,odb=odb)

@app.route("/shoppingcart/<username>/<sid>",methods=["GET","POST"])
def shoppingcart(username,sid):
    tdb=temp_database.query.all()
    total=0
    ttdb=tdb
    for row in ttdb:
        total+=int(row.price)
    if request.method=="POST":
        pickuptime=request.form["pickuptime"]
        tdb=temp_database.query.all()
        idb=inventory_database.query.all()
        sid=int(sid)
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
        profit=0
        for row in ttdb:
            p=p+f"{row.id}-{row.name}({row.qty})({row.price}),"
            total+=int(row.price)
            for r in idb:
                if int(r.item_id)==int(row.id):
                    profit+=(r.item_selling_price-r.item_costprice)*row.qty
        row=stores_orders_database(store_order_id=k+1,store_order_details=p,store_order_total=total,store_id=sid,store_order_profit_total=profit)
        db.session.add(row)
        db.session.commit()
        udb=user_database.query.all()
        customer_id=0
        for row in udb:
            if row.user_name==username:
                customer_id=int(row.sno)
                break
        row=orders_database(sno=k+1,customer_id=customer_id,store_order_details=p,store_order_total=total,store_id=sid,store_order_profit_total=profit,pickup=pickuptime)
        db.session.add(row)
        db.session.commit()
        
        return redirect(url_for("customerorderconfirmationpage",username=username))
    return render_template("shoppingcart.html",username=username,sid=int(sid),tdb=tdb,gtotal=total)
"""................................................................................................."""
"""................................................................................................."""
"""................................................................................................."""

if __name__=="__main__":
    app.run(debug=True)
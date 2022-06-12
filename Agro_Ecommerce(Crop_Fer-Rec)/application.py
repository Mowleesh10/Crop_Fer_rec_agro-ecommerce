import os
import uuid
from flask import Flask, session,render_template,request, Response, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from db import db_init, db
from models import  User, Product
from datetime import datetime
from flask_session import Session
from helpers import login_required

from flask import Flask, render_template, request
import pickle
import numpy as np
from collections import Counter

model_cr_dt = pickle.load(open('cr_dt.pkl','rb'))
model_cr_kn = pickle.load(open('cr_kn.pkl','rb'))
model_cr_rf = pickle.load(open('cr_rf.pkl','rb'))
model_cr_svm = pickle.load(open('cr_svm.pkl','rb'))
model_cr_lr = pickle.load(open('cr_lr.pkl','rb'))
model_cr_nb = pickle.load(open('cr_nb.pkl','rb'))

model_fr_kn = pickle.load(open('fr_knn.pkl','rb'))
model_fr_rf = pickle.load(open('fr_rf.pkl','rb'))
model_fr_svm = pickle.load(open('fr_svm.pkl','rb'))

app = Flask(__name__)

@app.route('/crop')
def crop():
    return render_template('crop.html')

@app.route('/recommend_crop', methods=['POST'])
def crop_rec():
    data1 = request.form['cra']
    data2 = request.form['crb']
    data3 = request.form['crc']
    data4 = request.form['crd']
    data5 = request.form['cre']
    data6 = request.form['crf']
    data7 = request.form['crg']
    arr = np.array([[data1, data2, data3, data4, data5, data6, data7]])

    pred_cr_dt = model_cr_dt.predict(arr)
    pred_cr_kn = model_cr_kn.predict(arr)
    pred_cr_rf = model_cr_rf.predict(arr)
    pred_cr_svm = model_cr_svm.predict(arr)
    pred_cr_lr = model_cr_lr.predict(arr)
    pred_cr_nb = model_cr_nb.predict(arr)

    a = [pred_cr_dt[0], pred_cr_kn[0], pred_cr_rf[0], pred_cr_svm[0], pred_cr_lr[0], pred_cr_nb[0]]

    c = Counter(a)
    mc = [key for key, val in c.most_common(3)]
    return render_template('crrec.html',trec = mc,rcdt=pred_cr_dt, rckn=pred_cr_kn, rcrf=pred_cr_rf, rcsvm=pred_cr_svm, rclr = pred_cr_lr, rcnb = pred_cr_nb)

@app.route('/fertilizer')
def fer():
    return render_template('fertilizer.html')

@app.route('/recommend_fer', methods=['POST'])
def fer_rec():
    data1 = request.form['fra']
    data2 = request.form['frb']
    data3 = request.form['frc']
    data4 = request.form['frstype']
    data5 = request.form['frctype']
    data6 = request.form['frf']
    data7 = request.form['frg']
    data8 = request.form['frh']
    arr = np.array([[data1, data2, data3, data4, data5, data6, data7,data8]])

    #pred_cr_dt = model_cr_dt.predict(arr)
    pred_fr_kn = model_fr_kn.predict(arr)
    pred_fr_rf = model_fr_rf.predict(arr)
    pred_fr_svm = model_fr_svm.predict(arr)
    #pred_cr_lr = model_cr_lr.predict(arr)
    #pred_cr_nb = model_cr_nb.predict(arr)

    a = [ pred_fr_kn[0], pred_fr_rf[0], pred_fr_svm[0]]

    c = Counter(a)
    mc = [key for key, val in c.most_common(3)]
    return render_template('ferrec.html',trec = mc,rckn=pred_fr_kn, rcrf=pred_fr_rf, rcsvm=pred_fr_svm)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#static file path
@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

#signup as merchant
@app.route("/signup", methods=["GET","POST"])
def signup():
	if request.method=="POST":
		session.clear()
		password = request.form.get("password")
		repassword = request.form.get("repassword")
		if(password!=repassword):
			return render_template("error.html", message="Passwords do not match!")

		#hash password
		pw_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
		
		fullname = request.form.get("fullname")
		username = request.form.get("username")
		#store in database
		new_user =User(fullname=fullname,username=username,password=pw_hash)
		try:
			db.session.add(new_user)
			db.session.commit()
		except:
			return render_template("error.html", message="Username already exists!")
		return render_template("login.html", msg="Account created!")
	return render_template("signup.html")

#login as merchant
@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method=="POST":
		session.clear()
		username = request.form.get("username")
		password = request.form.get("password")
		result = User.query.filter_by(username=username).first()
		print(result)
		# Ensure username exists and password is correct
		if result == None or not check_password_hash(result.password, password):
			return render_template("error.html", message="Invalid username and/or password")
		# Remember which user has logged in
		session["username"] = result.username
		return redirect("/home")
	return render_template("login.html")

#logout
@app.route("/logout")
def logout():
	session.clear()
	return redirect("/login")

#view all products
@app.route("/")
def index():
	rows = Product.query.all()
	return render_template("index.html", rows=rows)

#merchant home page to add new products and edit existing products
@app.route("/home", methods=["GET", "POST"], endpoint='home')
@login_required
def home():
	if request.method == "POST":
		image = request.files['image']
		filename = str(uuid.uuid1())+os.path.splitext(image.filename)[1]
		image.save(os.path.join("static/images", filename))
		category= request.form.get("category")
		name = request.form.get("pro_name")
		description = request.form.get("description")
		price_range = request.form.get("price_range")
		contact = request.form.get("contact")
		address = request.form.get("address")
		new_pro = Product(category=category,name=name,description=description,price_range=price_range,address=address,contact=contact,filename=filename, username=session['username'])
		db.session.add(new_pro)
		db.session.commit()
		rows = Product.query.filter_by(username=session['username'])
		return render_template("home.html", rows=rows, message="Product added")
	
	rows = Product.query.filter_by(username=session['username'])
	return render_template("home.html", rows=rows)

#when edit product option is selected this function is loaded
@app.route("/edit/<int:pro_id>", methods=["GET", "POST"], endpoint='edit')
@login_required
def edit(pro_id):
	#select only the editing product from db
	result = Product.query.filter_by(pro_id = pro_id).first()
	if request.method == "POST":
		#throw error when some merchant tries to edit product of other merchant
		if result.username != session['username']:
			return render_template("error.html", message="You are not authorized to edit this product")
		category= request.form.get("category")
		name = request.form.get("pro_name")
		description = request.form.get("description")
		price_range = request.form.get("price_range")
		contact = request.form.get("contact")
		address = request.form.get("address")
		result.category = category
		result.name = name
		result.description = description
		result.contact = contact
		result.address = address
		result.price_range = price_range
		db.session.commit()
		rows = Product.query.filter_by(username=session['username'])
		return render_template("home.html", rows=rows, message="Product edited")
	return render_template("edit.html", result=result)
@app.route("/delete/<int:pro_id>", methods=["GET", "POST"], endpoint='delete')
@login_required
def delete(pro_id):
	#select only the editing product from db
	result = Product.query.filter_by(pro_id = pro_id).first()
	db.session.delete(result)
	db.session.commit()
	rows = Product.query.filter_by(username=session['username'])
	return render_template("home.html", rows=rows, message="Product deleted")
	#return render_template("edit.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)

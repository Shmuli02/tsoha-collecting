from typing import Tuple
from flask.app import Flask
from app import app

from flask import render_template, request, redirect, session, url_for, flash
from werkzeug.utils import secure_filename
import os
import coins, users

UPLOAD_FOLDER = './static/img/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/admin")
def admin_index():
  if users.is_admin():
    return render_template("admin_index.html")
  else:
    flash({'code':1,'message':'Pääsy kielletty'})
    return redirect("/")

@app.route("/admin/coin")
def admin_coin():
  if users.is_admin():
    all_coins = coins.get_all_coins()
    return render_template("admin_coin.html", all_coins=all_coins)
  else:
    flash({'code':1,'message':'Pääsy kielletty'})
    return redirect('/')

@app.route("/admin/coin/<int:id>")
def admin_coin_id(id):
  if users.is_admin():
    coin = coins.get_coin_by_id(id)
    if coin is False:
      flash({'code':1,'message':'Virheellinen kolikko id'})
      return redirect('/')
    else:
      return render_template("admin_coin_id.html",coin=coin)
  else:
    flash({'code':1,'message':'Pääsy kielletty'})
    return redirect('/')

@app.route("/admin/collection")
def admin_collection():
  if users.is_admin():
    all_collections = coins.get_all_collections()
    return render_template("admin_collection.html",all_collections=all_collections)
  else:
    flash({'code':1,'message':'Pääsy kielletty'})
    return redirect('/')

@app.route("/admin/collection/<int:id>")
def admin_collection_id(id):
  if users.is_admin():
    collection = coins.get_collection_by_id(id)
    if collection is False:
      return redirect('/')
    else:
      return render_template("admin_collection_id.html",collection=collection)
  else:
    flash({'code':1,'message':'Pääsy kielletty'})
    redirect('/')

@app.route("/coin")
def coin():
  all_coins = coins.get_all_coins()
  if users.login():
    user_id = users.get_userid_by_username(session["username"])
    coins_user_own = coins.get_coins_user_own(user_id)
    return render_template("coins.html", all_coins=all_coins,coins_user_own = coins_user_own)
  else:
    return render_template("coins.html", all_coins=all_coins)

@app.route("/coin/<int:id>")
def coin_id(id):
  coin = coins.get_coin_by_id(id)
  if coin is False:
    return redirect('/')
  else:
    return render_template("coin_id.html",coin=coin)

@app.route("/collection/<int:id>")
def collection_id(id):
  collection = coins.get_collection_by_id(id)
  if collection is False:
    return redirect('/')
  else:
    return render_template("collection_id.html",collection=collection)

@app.route("/collection")
def collection():
  all_collections = coins.get_all_collections()
  return render_template("collection.html",all_collections=all_collections)





@app.route("/new_coin", methods=["POST","GET"])
def new_coin():
  if request.method == "GET":
    if users.is_admin():
      countries = coins.get_countries()
      materials = coins.get_materials()
      currencies = coins.get_currencies()
      all_coins = coins.get_all_coins()
      return render_template("admin_new_coin.html",countries=countries,materials=materials,currencies=currencies,all_coins=all_coins)
    else:
      return redirect('/')
  if request.method == "POST":
    add_coin = True
    if users.is_admin():
      img_url = ''
      ### Kuvien tallennus toimii paikallisesti, mutta ei herokussa. Joten syötteenä linkki kuvaan ###

      
      # if 'file' not in request.files:
      #   pass
      # file = request.files['file']
      # if file.filename == '':
      #   pass
      # if file and allowed_file(file.filename):
          # filename = secure_filename(file.filename)
          # img_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
          # file.save(img_url)
          # img_url = img_url[1:] #remove the dot from the link
      img_url = request.form["image_url"]
      country = request.form["country"]
      year = request.form["year"]
      mintage = request.form["mintage"]
      currency = request.form["currency"]
      value = request.form["value"]
      name = request.form["name"]
      description = request.form["description"]
      material = request.form["material"]
      public = request.form["public"]
    else:
      flash({'code':1,'message':'Pääsy kielletty'})
      return redirect('/')

    if country == '':
      flash({'code':1,'message':'Valitse maa'})
      add_coin = False
    if year == '':
      add_coin = False
      flash({'code':1,'message':'Valitse vuosi'})
    if currency == '':
      flash({'code':1,'message':'Valitse valuutta'})
      add_coin = False
    if value == '':
      flash({'code':1,'message':'Syötä arvo'})
      add_coin = False
    try:
      if int(value) < 0:
        flash({'code':1,'message':'Väärä arvo'})
        add_coin = False
    except:
      pass
    if name == '' or len(name)>100:
      flash({'code':1,'message':'Virhe nimessä'})
      add_coin = False
    if description == '':
      flash({'code':1,'message':'Virhe kuvauksessa'})
      add_coin = False
    if material == '':
      flash({'code':1,'message':'Valitse materiaali'})
      add_coin = False

    if add_coin is True:
      coins.add_new_coin(name,description,country,value,currency,material,public,img_url,mintage,year)
      flash({'code':2,'message':'Kolikon lisäys onnistui'})
      return redirect("/new_coin")
    else:
      return redirect("/new_coin")


@app.route("/new_collection", methods=["POST","GET"])
def new_collection():
  if request.method == "GET":
    if users.is_admin():
      all_coins = coins.get_all_coins()
      return render_template("admin_new_collection.html", all_coins=all_coins)
    else:
      return redirect("/")
  if request.method == "POST":
    add_collection = True
    if users.is_admin():
      if 'coin-to-collection' in request.form:
        collection_coins = request.form.to_dict(flat=False)['coin-to-collection']
      else:
        collection_coins = []
      name = request.form["name"]
      description = request.form["description"]
      public = request.form["public"]
    else:
      return redirect('/')
    if name == '' or len(name) >100:
      flash({'code':1,'message':'Virhe nimessä'})
      add_collection = False
    if description == '' or len(description)>5000:
      flash({'code':1,'message':'Virhe kuvauksessa'})
      add_collection = False
    if add_collection is True:
      author = users.get_userid_by_username(session["username"])
      coins.add_new_collection(name,description,public,collection_coins,author)
      flash({'code':2,'message':'Kokoelma lisätty'})
      return redirect("/new_collection")
    else:
      return redirect("/new_collection")

@app.route("/add_own_coin", methods=["POST"])
def add_own_coin():
  if request.method == "POST":
    try:
      username = session["username"]
    except:
      flash({'code':1,'message':'Kirjaudu sisään'})
      return redirect("/")
    user_id = users.get_userid_by_username(username)
    try:
      coin = request.form["Coin name"]
    except:
      flash({'code':1,'message':'Virhe kolikossa'})
      return redirect("/coin")
    coin_id = coins.get_coinid_by_coin_name(coin)
    try:
      amount = int(request.form["amount"])
    except:
      flash({'code':1,'message':'Virhe määrässä'})
      return redirect("/coin")
    if amount < 0:
      flash({'code':1,'message':'Virhe määrässä'})
      return redirect("/coin")
    print(user_id,coin_id,amount)
    coins.add_own_coin(user_id,coin_id,amount)
    if amount == 1:
      flash({'code':2,'message':'Kolikko lisätty'})
    else:
      flash({'code':2,'message':'Kolikot lisätty'})
    return redirect("/coin")


@app.route("/login",methods=["POST","GET"])
def login():
  if request.method == "GET":
    return render_template("login.html")
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username,password):
      return redirect("/")
    else:
      flash({'code':1,'message':'Väärä käyttäjätunnus tai salasana'})
      return render_template("login.html")

@app.route("/logout")
def logout():
  del session["username"]
  return redirect("/")

@app.route("/register", methods=["POST","GET"])
def register():
  if request.method == "GET":
    return render_template("register.html")
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]
    if users.register(username,password,password2):
      return redirect("/login")
    else:
      return render_template("register.html")

@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html")
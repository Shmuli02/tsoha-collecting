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
  return render_template("admin_index.html")

@app.route("/admin/coin")
def admin_coin():
  all_coins = coins.get_all_coins()
  return render_template("admin_coin.html", all_coins=all_coins)

@app.route("/admin/collection")
def admin_collection():
  all_collections = coins.get_all_collections()
  return render_template("admin_collection.html",all_collections=all_collections)

@app.route("/coin")
def coin():
  all_coins = coins.get_all_coins()
  return render_template("coins.html", all_coins=all_coins)

@app.route("/coin/<int:id>")
def admin_coin_id(id):
  coin = coins.get_coin_by_id(id)
  if coin is False:
    return redirect('/')
    
  else:
    return render_template("coin_id.html",coin=coin)

@app.route("/admin/collection/<int:id>")
def admin_collection_id(id):
  collection = coins.get_collection_by_id(id)
  if collection is False:
    return redirect('/')
  else:
    return render_template("admin_collection_id.html",collection=collection)

@app.route("/new_coin", methods=["POST","GET"])
def new_coin():
  if request.method == "GET":
    countries = coins.get_countries()
    materials = coins.get_materials()
    currencies = coins.get_currencies()
    all_coins = coins.get_all_coins()
    return render_template("admin_new_coin.html",countries=countries,materials=materials,currencies=currencies,all_coins=all_coins)
  if request.method == "POST":
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
    coins.add_new_coin(name,description,country,value,currency,material,public,img_url,mintage,year)
    return redirect("/admin/coin")

@app.route("/new_collection", methods=["POST","GET"])
def new_collection():
  if request.method == "GET":
    all_coins = coins.get_all_coins()
    return render_template("admin_new_collection.html", all_coins=all_coins)
  if request.method == "POST":
    if 'coin-to-collection' in request.form:
      collection_coins = request.form.to_dict(flat=False)['coin-to-collection']
    else:
      collection_coins = []
    name = request.form["name"]
    description = request.form["description"]
    public = request.form["public"]
    author = users.get_userid_by_username(session["username"])
    coins.add_new_collection(name,description,public,collection_coins,author)
    return redirect("/new_collection")

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
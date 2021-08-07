from app import app

from flask import render_template, request, redirect, session
from db import db


@app.route("/")
def index():
  return render_template("index.html")

@app.route("/admin")
def admin_index():
  return render_template("admin_index.html")

@app.route("/admin/coin")
def admin_coin():
  return render_template("admin_coin.html", countries=["maa1","maa2"])

@app.route("/admin/coin/<int:id>")
def admin_coin_id(id):
  return render_template("admin_coin_id.html")

@app.route("/new_coin", methods=["POST"])
def new_coin():
  country = request.form["country"]
  year = request.form["year"]
  currency = request.form["currency"]
  value = request.form["value"]
  name = request.form["name"]
  description = request.form["description"]
  material = request.form["material"]
  print(country)
  return redirect("/admin/coin")
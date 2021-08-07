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
  return render_template("admin_coin.html")

@app.route("/admin/coin/<int:id>")
def admin_coin_id(id):
  return render_template("admin_coin_id.html")

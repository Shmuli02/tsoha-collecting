from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import messages

def login(username,password):
  session["username"] = username

def register(username, password):
  hash_value = generate_password_hash(password)
  sql = "INSERT INTO users (username,password,admin) VALUES (:username,:password,0)"
  db.session.execute(sql,{"username":username,"password":hash_value})
  db.session.commit()
  return 
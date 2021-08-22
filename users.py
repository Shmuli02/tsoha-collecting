from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import coins

def login(username,password):
  sql = "SELECT id, password, admin FROM users WHERE username=:username"
  result = db.session.execute(sql, {"username":username})
  user = result.fetchone()
  if not user:
    return False
  else:
    hash_value = user.password
    if check_password_hash(hash_value,password):
      session["username"] = username
      session["admin"] = user.admin
      return True
    else:
      return False
  

def register(username, password,password2):
  if password == password2:
    if username != '' and password != '':
      hash_value = generate_password_hash(password)
      sql = """
        INSERT INTO 
          users (username,password,admin) 
        VALUES 
          (:username,:password,0)
        """
      db.session.execute(sql,{"username":username,"password":hash_value})
      db.session.commit()
      return True
    else:
      return False
  else:
    return False

def get_userid_by_username(username):
  sql = "SELECT id, username FROM users WHERE username=:username"
  result = db.session.execute(sql,{"username":username})
  user = result.fetchall()
  return user[0][0]
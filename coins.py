from db import db
from flask import session

def get_countries():
  sql = "SELECT country FROM country"
  result = db.session.execute(sql)
  return result.fetchall()

def add_new_coin(name,description,country,value,currency,material):
  sql = "INSERT INTO coin_data (name,description,country,value,currency,material) VALUES (:name,:description,:country,:value,:currency,:material)"
  db.session.execute(sql,{"name":name,"description":description,"country":country,"value":value,"currency":currency,"material":material})
  db.session.commit()
  return

def get_materials():
  sql = "SELECT material FROM material"
  result = db.session.execute(sql)
  return result.fetchall()

def get_currencies():
  sql = "SELECT currency FROM currency"
  result = db.session.execute(sql)
  return result.fetchall()

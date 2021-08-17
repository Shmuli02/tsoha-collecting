from db import db
from flask import session

def get_countries():
  sql = "SELECT id,country FROM country"
  result = db.session.execute(sql)
  result_list = [{'id':item[0],'country':item[1]} for item in result.fetchall()]
  return result_list

def add_new_coin(name,description,country,value,currency,material,public):
  sql = """
    INSERT INTO 
      coin_data (name,description,country,value,currency,material) 
    VALUES 
      (:name,:description,:country,:value,:currency,:material)
    """
  db.session.execute(sql,{"name":name,"description":description,"country":country,"value":value,"currency":currency,"material":material})
  db.session.commit()
  return

def get_materials():
  sql = "SELECT id,material FROM material"
  result = db.session.execute(sql)
  result_list = [{'id':item[0],'material':item[1]} for item in result.fetchall()]
  return result_list

def get_currencies():
  sql = "SELECT id, currency FROM currency"
  result = db.session.execute(sql)
  result_list = [{'id':item[0],'currency':item[1]} for item in result.fetchall()]
  return result_list

def get_all_coins():
  sql = """
    SELECT 
      coin.id,coin.name,coin.description,country.country,coin.value,currency.currency,material.material
    FROM 
      coin_data AS coin
    INNER JOIN 
      country ON coin.country = country.id
    INNER JOIN
      material ON coin.material = material.id
    INNER JOIN
      currency ON coin.currency = currency.id
    """
  result = db.session.execute(sql)
  coin_list = [{'id':col1,'name':col2,'description':col3,'country':col4,'value':col5,'currency':col6,'material':col7} for (col1,col2,col3,col4,col5,col6,col7) in result.fetchall()]
  
  return coin_list

def get_coin_by_id(id):
  all_coins = get_all_coins()
  coin = list(filter(lambda x: x['id'] == id, all_coins))
  if len(coin) == 0:
    return False
  else:
    return coin[0]
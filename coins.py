from db import db
from flask import session
import ast
import users

def get_countries():
  sql = "SELECT id,country FROM country"
  result = db.session.execute(sql)
  result_list = [{'id':item[0],'country':item[1]} for item in result.fetchall()]
  return result_list

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


def add_new_coin(name,description,country,value,currency,material,public,img_url,mintage,year):
  if img_url == "":
    img_url = "/static/img/no-image-available.jpg"
  sql = """
    INSERT INTO 
      coin_data (name,description,country_id,value,currency_id,material_id,mintage,year,public,image_url) 
    VALUES 
      (:name,:description,:country_id,:value,:currency_id,:material_id,:mintage,:year,:public,:image_url)
    """
  db.session.execute(sql,{"name":name,"description":description,"country_id":country,"value":value,"currency_id":currency,"material_id":material,"mintage":mintage,"year":year,"public":public,"image_url":img_url})
  db.session.commit()
  return

def add_own_coin(user_id,coin_id,amount):
  sql = """
    INSERT INTO
      coin_user_own (coin_id,amount,user_id)
    VALUES
      (:coin_id,:amount,:user_id)
  """
  db.session.execute(sql,{'user_id':user_id,'coin_id':coin_id,'amount':amount})
  db.session.commit()
  return

def get_all_coins():
  sql = """
    SELECT 
      coin.id,coin.name,coin.description,country.country,coin.value,currency.currency,material.material,coin.image_url,coin.mintage,coin.year
    FROM 
      coin_data AS coin
    INNER JOIN 
      country ON coin.country_id = country.id
    INNER JOIN
      material ON coin.material_id = material.id
    INNER JOIN
      currency ON coin.currency_id = currency.id
    """
  result = db.session.execute(sql)
  coin_list = [{'id':col1,'name':col2,'description':col3,'country':col4,'value':col5,'currency':col6,'material':col7,'image_url':col8,'mintage':col9,'year':col10} for (col1,col2,col3,col4,col5,col6,col7,col8,col9,col10) in result.fetchall()]
  
  return coin_list

def get_coin_by_id(id):
  all_coins = get_all_coins()
  coin = list(filter(lambda x: x['id'] == id, all_coins))
  if len(coin) == 0:
    return False
  else:
    return coin[0]

def get_coinid_by_coin_name(coin_name):
  sql = "SELECT id, name FROM coin_data WHERE name=:name"
  result = db.session.execute(sql,{"name":coin_name})
  user = result.fetchall()
  return user[0][0]

def get_coins_user_own(user_id):
  sql = """
  SELECT
    coin_id,COUNT(amount)
  FROM
    coin_user_own
  WHERE
    user_id=:user_id
  GROUP BY
    coin_id
  """
  result = db.session.execute(sql,{'user_id':user_id})
  coins_user_own = [{'coin_id':col1,'amount':col2} for (col1,col2) in result.fetchall()]
  coins_user_own_with_coin_data = []
  for coin in coins_user_own:
    coin_data = get_coin_by_id(coin['coin_id'])
    coin_data['amount'] = coin['amount']
    coins_user_own_with_coin_data.append(coin_data)
  return coins_user_own_with_coin_data


def add_new_collection(name,description,public,collection_coins,author):
  sql = """
    INSERT INTO
      coin_collection (name,description,public,coins,author_id)
    VALUES
      (:name,:description,:public,:collection_coins,:author)
  """
  db.session.execute(sql,{"name":name,"description":description,"public":public,"collection_coins":str(collection_coins),"author":author})
  db.session.commit()
  return

def get_all_collections():
  sql = """
    SELECT
      c.id,c.name,c.description,c.public,c.coins,c.author_id
    FROM
      coin_collection as c
  """
  result = db.session.execute(sql)
  collection_list = [{'id':col1,'name':col2,'description':col3,'public':col4,'coins':col5,'author_id':col6} for (col1,col2,col3,col4,col5,col6) in result.fetchall()]
  return collection_list

def get_collection_by_id(id):
  all_collections = get_all_collections()
  collection = list(filter(lambda x: x['id'] == id, all_collections))
  if len(collection) == 0:
    return False
  else:
    collection = collection[0]
    user_own_coins_id = []
    try:
      if session["username"]:
        user_id = users.get_userid_by_username(session["username"])
        user_own_coins = get_coins_user_own(user_id)
        user_own_coins_id = [coin['id'] for coin in user_own_coins] # käyttäjän omistamien kolikoiden id
    except:
      pass

    coins = ast.literal_eval(collection['coins'])
    coins_int = [int(x) for x in coins]
    all_collection_coins = [] # Kaikki kokoelman kolikot
    collection_coins_user_not_own = [] #kolikot jotka käyttäjä ei omista jos kirjautunut
    collection_coins_user_own = [] # kokoelman kolikoista ne jotka käyttäjä omistaa
    for id in coins_int:
      coin = get_coin_by_id(id)
      all_collection_coins.append(coin)
      if id in user_own_coins_id:
        collection_coins_user_own.append(coin)
      else:
        collection_coins_user_not_own.append(coin)
    collection['all_collection_coins'] = all_collection_coins
    collection['collection_coins_user_own'] = collection_coins_user_own
    collection['collection_coins_user_not_own'] = collection_coins_user_not_own

    return collection
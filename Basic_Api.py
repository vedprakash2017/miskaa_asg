from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

#change with your database name 
app.config['MONGO_DBNAME'] = 'cart' 

#change with your database uri 
app.config['MONGO_URI'] = 'mongodb://localhost:27017/cart'

mongo = PyMongo(app)
#To get all items from cart
@app.route('/cart', methods=['GET'])
def get_all_items():
  item = mongo.db.items
  output = []
  for s in item.find():
    output.append({'name' : s['name'], 'description' : s['description'] , 'price' : s['price'], 'id': str(s['_id'])})
  return jsonify({'result' : output})

#to add a item in cart
@app.route('/add', methods=['POST'])
def add_items():
  item = mongo.db.items
  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  item_id = item.insert({'name': name, 'description' : description, 'price' : price })
  new_item = item.find_one({'_id': item_id })
  output = {'name' : new_item['name'], 'description' : new_item['description'], 'price' : new_item['price'],'id':str(new_item['_id'])}
  return jsonify({'result' : output})

#to delete a item in cart by using _id (as it will unique for all items) you can get it by database
@app.route('/del/<dupId>', methods=['DELETE'])
def get_one_item(dupId):
  item = mongo.db.items
  s = item.find_one( {"_id" : ObjectId(str(dupId))} )
  print(s)
  if s:
    item.delete_one( {"_id" : ObjectId(str(dupId))} )
    output = []
    for s in item.find():
        output.append({'name' : s['name'], 'description' : s['description'] , 'price' : s['price'], 'id': str(s['_id'])})
  else:
    output = "No such item"
  return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True)
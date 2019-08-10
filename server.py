from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/test'

mongo = PyMongo(app)

if mongo:
  print("The database exists.")
if not mongo.db.users:
    print("The table exists")
    mongo.db.users.insert_one({'username': 'user', 'password': 'password'})
  
print(mongo)

# rest api to get all users
@app.route('/api/user', methods=['GET'])
def get_all_users():
  users = mongo.db.users
  output = []
  for user in users.find():
    print(user)  
    output.append({'username' : user['username'], 'password' : user['password']})
  return jsonify({'result' : output})

 # rest api to get a single user
@app.route("/api/user/<id>", methods=["GET"])
def user_detail(id):
  users = mongo.db.users
  user = users.find_one({'id' : id})
  if user:
    output = {'username' : user['username'], 'password' : user['password']}
  else:
    output = "No such user"
  return jsonify({'result' : output})

#rest api to create a new user
@app.route('/api/user', methods=['POST'])
def add_user():
  users = mongo.db.users
  username = request.json['username']
  password = request.json['password']
  users.insert_one({'username': username, 'password': password})
  return jsonify({'One record added'})

#rest api to update a user
@app.route("/api/user/<username>", methods=["PUT"])
def user_update(username):
    users = mongo.db.users
    changedusername = request.json['username']
    changedpassword = request.json['password']
    myquery = { "username": username }
    newvalues = { "$set": {'username': changedusername, 'password': changedpassword} }
    users.update_one(myquery,newvalues)
    return jsonify("record updated ")

#rest api to delete a user
@app.route("/api/user/<username>", methods=["DELETE"])
def user_delete(username):
    users = mongo.db.users
    myquery = { "username": username }
    users.delete_one(myquery)
    return jsonify("record deleted ")

if __name__ == '__main__':
    app.run(debug=True)

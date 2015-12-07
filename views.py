import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from flask import Flask, request, jsonify, Response
import re
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
connection = MongoClient('mongodb://npwm_admin:pass123@ds061984.mongolab.com:61984/heroku_4j8g2kcv')
db = connection.heroku_4j8g2kcv

@app.route("/cuisines", methods=['GET'])
def cuisines():
	arr = []
	c = db.restaurant.find().distinct("cuisine")
	json_docs = [json.dumps(document, default=json_util.default) for document in c]
	if len(json_docs) is not 0:
		for jsondump in json_docs:
			arr.append(json.loads(jsondump))
		return Response(json.dumps({
			'success': True,
			'response': arr
			}), status=200, content_type='application/json')
	else:
		return Response(json.dumps({
			'success': False,
			'response': 'No Data'
			}))


@app.route("/search", methods=['GET'])
def search():
	q =  request.args['q']
	arr = []
	reg = r".*(?i)"+re.escape(q)+".*"
	x = db.restaurant.find({"name" : {'$regex': reg}})
	json_docs = [json.dumps(document, default=json_util.default) for document in x]
	if len(json_docs) is not 0:
		for jsondump in json_docs:
			arr.append(json.loads(jsondump))
		return Response(json.dumps({
			'success': True,
			'response': arr
			}), status=200, content_type='application/json')
	else:
		return Response(json.dumps({
			'success': False,
			'response': 'No Data'
			}))

@app.route('/restaurant/<restaurant_id>', methods=['GET', 'POST'])
def tweet_detail(restaurant_id=None):
	if request.method == 'GET':
		tweet = db.restaurant.find({"restaurant_id": restaurant_id})
		json_docs = []
		for doc in tweet:
			json_doc = json.dumps(doc, default=json_util.default)
			json_docs.append(json.loads(json_doc))
		return Response(json.dumps({
				'success': True,
				'response': json_docs
				}), status=200, content_type='application/json')
	elif request.method == 'POST':
		comments = [request.form['comment']]
		print comments
		tweet = db.restaurant.update({"restaurant_id": restaurant_id}, {"$addToSet": {"review": {'$each': comments}}},  upsert=True)
		updated = db.restaurant.find({"restaurant_id": restaurant_id})
		json_docs = []
		for doc in updated:
			json_doc = json.dumps(doc, default=json_util.default)
			json_docs.append(json.loads(json_doc))
		return Response(json.dumps({
				'success': True,
				'response': json_docs
				}), status=200, content_type='application/json')


if __name__ == "__main__":
	app.debug = True
	app.run()


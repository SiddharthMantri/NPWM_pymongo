import pymongo
from pymongo import MongoClient
import json
from bson import json_util
from flask import Flask, request, jsonify, Response
import re
from flask.ext.cors import CORS

app = Flask(__name__)
CORS(app)
connection = MongoClient('mongodb://bhavin:pass123@ds059694.mongolab.com:59694/npm_db')
db = connection.npm_db
@app.route("/search", methods=['GET'])
def search():
	q =  request.args['q']
	arr = []
	reg = r"\b(?=\w)" + re.escape(q) + r"\b(?!\w)"
	json_docs = [json.dumps(document, default=json_util.default) for document in db.Restaurants.find({"name" : {'$regex': reg}})]
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

@app.route('/tweet/<comment_id>', methods=['GET', 'POST'])
def tweet_detail(comment_id=None):
	if request.method == 'GET':
		tweet = db.restaurant.find({"id": int(comment_id)})
		json_docs = []
		for doc in tweet:
			json_doc = json.dumps(doc, default=json_util.default)
			json_docs.append(json.loads(json_doc))
		return Response(json.dumps({
				'success': True,
				'response': json_docs
				}), status=200, content_type='application/json')
	elif request.method == 'POST':
		tweet = db.tweets.update({"id": int(comment_id)}, {"$addToSet": {"review": request.form['comment']}})
		updated = db.tweets.find({"id": int(comment_id)})
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


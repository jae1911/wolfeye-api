from flask import Flask, jsonify, request

import datetime
import redis

import db

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

@app.before_first_request
def init_db_connection():
	db.database.connect()
	db.database.create_tables([db.Search])

@app.route('/api/ping')
def api_ping():
	""" Pings the API to know the status
	"""
	return jsonify({'status': 'ok'})

@app.route('/api/total_db')
def api_total_db():
	""" Gets the total row count of the DB
	"""
	count = 0
	cache = False
	cached_result = r.get('total_count')
	if cached_result:
		count = int(cached_result)
		cache = True
	else:
		res = db.Search.select().count()
		if res:
			count = res
			r.set('total_count', res)

	return jsonify({'count': count, 'cache-hit': cache})

@app.route('/api/crawler/add', methods=['POST'])
def api_crawler_add():
	""" Endpoint for the crawler to add URLs to the database
	"""

	data = request.json
	print(data)

	if not data:
		return jsonify({'err': 'invalid request'}), 400

	url = data.get('url')
	title = data.get('title')

	if not url or not title:
		return jsonify({'err': 'invalid request'}), 400

	existing_url = db.Search.select().where(db.Search.url == url).count()
	if existing_url > 0:
		return jsonify({'err': 'already exists'})

	new_result = db.Search(url=url, title=title, last_fetched=datetime.datetime.now())
	new_result.save()

	return jsonify({'success': 'ok'})

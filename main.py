from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler

import datetime
import redis
import time
import atexit

import db

app = Flask(__name__)

db.database.connect()
db.database.create_tables([db.Search, db.Token])

r = redis.Redis(host='localhost', port=6379, charset="utf-8", decode_responses=True)

def update_cache_count():
	count = 0
	res = db.Search.select().count()
	if res:
		count = res
		r.set('total_count', res)
	print(f'UPDATED COUNTS, NEW IS {count}')

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_cache_count, trigger="interval", minutes=30)
scheduler.start()

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

	token = data.get('token')
	if not token:
		return jsonify({'err': 'invalid request'}), 400

	try:
		current_token = db.Token.select().where(db.Token.token == token).get()
	except:
		current_token = None

	if not current_token:
		return jsonify({'err': 'unauthorized'}), 401
	elif current_token.expiry_date < datetime.datetime.now():
		return jsonify({'err': 'unauthorized'}), 401

	url = data.get('url')
	title = data.get('title')

	if not url or not title:
		return jsonify({'err': 'invalid request'}), 400

	try:
		existing_url = db.Search.select().where(db.Search.url == url).get()
	except:
		existing_url = None
	
	if existing_url:
		return jsonify({'err': 'already exists', 'fetched_on': existing_url.last_fetched})

	new_result = db.Search(url=url, title=title, last_fetched=datetime.datetime.now())
	new_result.save()

	return jsonify({'success': 'ok'})

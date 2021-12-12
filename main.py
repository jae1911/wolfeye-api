from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from playhouse.shortcuts import model_to_dict, dict_to_model

import datetime
import redis
import time
import atexit
import re
import json
import ast
import os
import requests

import db

app = Flask(__name__)

db.database.connect()
db.database.create_tables([db.Search, db.Token])

redis_host = os.environ.get('REDIS_HOST')
if redis_host:
	r = redis.Redis(host=redis_host, port=6379, charset="utf-8", decode_responses=True)
else:
	r = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)

def update_cache_count():
	count = 0
	res = db.Search.select().count()
	if res:
		count = res
		r.set('total_count', res)
	print(f'UPDATED COUNTS, NEW IS {count}')

def remove_old_instant_answers():
	for key in r.scan_iter("isearch_*"):
		print(key)
		r.delete(key)
	print("CLEANED INSTANT ANSWERS")

def remove_old_queries():
	for key in r.scan_iter("search_*"):
		print(key)
		r.delete(key)
	print("CLEANED QUERIES")

scheduler = BackgroundScheduler()
scheduler.add_job(func=update_cache_count, trigger="interval", minutes=30)
scheduler.add_job(func=remove_old_queries, trigger="interval", minutes=15)
scheduler.add_job(func=remove_old_instant_answers, trigger="interval", hours=1)
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

@app.route('/api/search', methods=['POST'])
def api_search():
	""" Search the database
	"""
	data = request.json

	if not data:
		return jsonify({'err': 'invalid request'}), 400

	query = data.get('query')

	if not query:
		return jsonify({'err': 'missing query'}), 400

	cache = False
	res = None

	query_trimmed = query.replace(' ', '_').replace('\'', '-')
	escaped_query = 'search_' + re.escape(query_trimmed)
	
	cached_result = r.get(escaped_query)
	if cached_result:
		res = json.loads(cached_result)
		cache = True
	else:
		matched_content = []

		first_pass = db.Search().select().where(db.Search.title.contains(query))
		for content in first_pass:
			match = {
				'title': content.title,
				'url': content.url
			}
			matched_content.append(match)

			res = matched_content

		exploded_query = query.split(' ')
		for shard in exploded_query:
			second_pass = db.Search().select().where(db.Search.title.contains(shard))

			for content in second_pass:
				already = False

				for stuff in matched_content:
					if content.url == stuff['url']:
						already = True

				if not already:
					match = {
						'title': content.title,
						'url': content.url
					}
					matched_content.append(match)

		r.set(escaped_query, str(json.dumps(matched_content)))

	return jsonify({'res': res, 'cache-hit': cache})

@app.route('/api/admin/get_all')
def api_admin_get_all():
	""" Get everything contained in the database
	"""
	data = request.json

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

	res = []
	everything_in_db = db.Search.select()

	for query in everything_in_db:
		query_dict = {
			'url': query.url,
			'title': query.title,
			'last_fetched': query.last_fetched
		}
		res.append(query_dict)

	return jsonify(res)

@app.route('/api/crawler/add', methods=['POST'])
def api_crawler_add():
	""" Endpoint for the crawler to add URLs to the database
	"""

	data = request.json

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

@app.route('/api/instant', methods=['POST'])
def api_instant():
	""" Instant answers (DDG API)
	"""
	data = request.json

	if not data:
		return jsonify({'err': 'invalid request'})

	query = data.get('query')

	if not query:
		return jsonify({'err': 'no query'})

	cache = False
	res = None

	query_trimmed = query.replace(' ', '_').replace('\'', '-')
	escaped_query = 'isearch_' + re.escape(query_trimmed)

	cached_result = r.get(escaped_query)
	if cached_result:
		res = json.loads(cached_result)
		cache = True
	else:
		ddg_api_query_url = f"https://api.duckduckgo.com/?q={query}&format=json"
		
		req = requests.get(ddg_api_query_url)

		if req:
			response = req.json()

			res = response

			r.set(escaped_query, str(json.dumps(response)))

	return jsonify({'res': res, 'cache-hit': cache})

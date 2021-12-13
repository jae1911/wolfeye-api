from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from playhouse.shortcuts import model_to_dict, dict_to_model
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from autocorrect import Speller

import datetime
import redis
import time
import atexit
import re
import json
import ast
import os
import requests
import logging

import db

app = Flask(__name__)

def get_remote_ip():
	return request.headers.get('X-Forwarded-For')

limiter = Limiter(
	app,
	key_func=get_remote_ip,
	default_limits=["20 per minute"]
)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

db.database.connect()
db.database.create_tables([db.Search, db.Token])

db.migrate_db()

redis_host = os.environ.get('REDIS_HOST')
if redis_host:
	r = redis.Redis(host=redis_host, port=6379, charset="utf-8", decode_responses=True)
else:
	r = redis.Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)

@app.route('/api/ping')
@limiter.exempt
def api_ping():
	""" Pings the API to know the status
	"""
	return jsonify({'status': 'ok'})

@app.route('/api/total_db')
@limiter.exempt
def api_total_db():
	""" Gets the total row count of the DB
	"""
	count = 0
	cache = False
	ttl = 0
	cached_result = r.get('total_count')
	if cached_result:
		count = int(cached_result)
		cache = True
		ttl = r.ttl('total_count')
	else:
		res = db.Search.select().count()
		if res:
			count = res
			time_to_expire_s = 1800
			r.set('total_count', res, ex=time_to_expire_s)

	return jsonify({'count': count, 'cache-hit': cache, 'ttl': ttl})

@app.route('/api/tocorrect', methods=['POST'])
@limiter.exempt
def api_tocorrect():
	""" Sends a correction of the provided string
	"""
	data = request.json

	if not data:
		return jsonify({'err': 'invalid query'}), 400

	string_base = data.get('string')

	if not string_base:
		return jsonify({'err': 'missing string'}), 400

	res = None
	cache = False
	ttl = 0
	corrected = False

	cached_result = r.get(string_base)
	if cached_result:
		res = cached_result
		cache = True
		corrected = True
		ttl = r.ttl(string_base)
	else:
		if string_base == 'a':
			final_ttl = 60 * 60 * 24 * 365 * 15
			r.set(string_base, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', ex=final_ttl)
		
		spell = Speller()
		res = spell(string_base)

		if res != string_base:
			corrected = True
			final_ttl = 60 * 60 * 24
			r.set(string_base, res, ex=final_ttl)

	return jsonify({'res': res, 'corrected': corrected, 'cache-hit': cache, 'ttl': ttl})


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
	ttl = 0

	query_trimmed = query.replace(' ', '_').replace('\'', '-')
	escaped_query = 'search_' + re.escape(query_trimmed)
	
	cached_result = r.get(escaped_query)
	if cached_result:
		res = json.loads(cached_result)
		cache = True
		ttl = r.ttl(escaped_query)
	else:
		matched_content = []

		first_pass = db.Search().select().where(db.Search.title.contains(query))
		for content in first_pass:
			match = {
				'title': content.title,
				'url': content.url,
				'description': content.description
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
						'url': content.url,
						'description': content.description
					}
					matched_content.append(match)

			third_pass = db.Search().select().where(db.Search.url.contains(shard))
			for content in third_pass:
				already = False

				for stuff in matched_content:
					if content.url == stuff['url']:
						already = True

				if not already:
					match = {
						'title': content.title,
						'url': content.url,
						'description': content.description
					}
					matched_content.append(match)

			fourth_pass = db.Search().select().where(db.Search.description.contains(shard))
			for content in fourth_pass:
				already = False

				for stuff in matched_content:
					if content.url == stuff['url']:
						already = True

				if not already:
					match = {
						'title': content.title,
						'url': content.url,
						'description': content.description
					}
					matched_content.append(match)

			if not matched_content:
				fifth_pass = db.Search().select().where(db.Search.url.contains(shard))
				for content in fifth_pass:
					match = {
						'title': content.title,
						'url': content.url,
						'description': content.description
					}

		time_to_expire_s = 900
		r.set(escaped_query, str(json.dumps(matched_content)), ex=time_to_expire_s)

	return jsonify({'res': res, 'cache-hit': cache, 'ttl': ttl})

@app.route('/api/admin/token/add', methods=['POST'])
@limiter.exempt
def api_admin_token_add():
	""" Adds a new token
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

	new_token = data.get('newtoken')

	if not new_token:
		return jsonify({'err': 'invalid request'}), 400

	expiry = data.get('expiry')

	if not expiry:
		expiry = datetime.datetime.now() + datetime.timedelta(days=5000)

	try:
		existing = db.Token.select().where(db.Token.token == new_token).get()
	except:
		existing = None
	if existing:
		return jsonify({'err': 'exists'})

	create_token = db.Token(token=new_token, expiry_date=expiry)
	create_token.save()

	return jsonify({'success': True})

@app.route('/api/admin/get_all')
@limiter.limit("2 per minute")
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
			'last_fetched': query.last_fetched,
			'description': query.description
		}
		res.append(query_dict)

	return jsonify(res)

@app.route('/api/crawler/add', methods=['POST'])
@limiter.exempt
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
	description = data.get('description')

	if not url or not title:
		return jsonify({'err': 'invalid request'}), 400

	if not description:
		description = 'No description provided for this website.'

	try:
		existing_url = db.Search.select().where(db.Search.url == url).get()
	except:
		existing_url = None

	if existing_url:

		if existing_url.description == description and existing_url.title == title:
			return jsonify({'err': 'already exists', 'fetched_on': existing_url.last_fetched})
		else:
			if existing_url.description != description:
				existing_url.description = description

			if existing_url.title != title:
				existing_url.title = title

			existing_url.last_fetched = datetime.datetime.now()
			existing_url.save()
			return jsonify({'success': 'ok'})

	new_result = db.Search(url=url, title=title, description=description, last_fetched=datetime.datetime.now())
	new_result.save()

	return jsonify({'success': 'ok'})

@app.route('/api/instant', methods=['POST'])
@limiter.limit("3 per minute")
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
	ttl = 0

	query_trimmed = query.replace(' ', '_').replace('\'', '-')
	escaped_query = 'isearch_' + re.escape(query_trimmed)

	cached_result = r.get(escaped_query)
	if cached_result:
		res = json.loads(cached_result)
		cache = True
		ttl = r.ttl(escaped_query)
	else:
		ddg_api_query_url = f"https://api.duckduckgo.com/?q={query}&format=json"
		
		req = requests.get(ddg_api_query_url)

		if req:
			response = req.json()

			res = response

			time_to_expire_s = 3600
			r.set(escaped_query, str(json.dumps(response)), ex=time_to_expire_s)

	return jsonify({'res': res, 'cache-hit': cache, 'ttl': ttl})

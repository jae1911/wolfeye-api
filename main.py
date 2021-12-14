""" Main file for the Wolfeye Search Engine API
"""

import datetime
import json
import logging
import os
import re
import redis
import requests

from flask import Flask, jsonify, request, abort
from flask_limiter import Limiter
from autocorrect import Speller

import db

app = Flask(__name__)

def get_remote_ip():
    """ Will return the IP of a user behind a reverse proxy (used by the rate limiter)
    """
    res = request.headers.get('X-Forwarded-For')

    if not res:
        res = request.remote_addr

    return res

limiter = Limiter(
    app,
    key_func=get_remote_ip,
    default_limits=["20 per minute"]
)

log = logging.getLogger('werkzeug')
app_log = logging.getLogger('wolfeye')
log.setLevel(logging.ERROR)
app_log.setLevel(logging.INFO)

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
        app_log.info(f'Using cached content for total_count; ttl {ttl}')
    else:
        res = db.Search.select().count()
        if res:
            count = res
            time_to_expire_s = 1800
            r.set('total_count', res, ex=time_to_expire_s)
            app_log.info(f'Cached total query with TTL at {time_to_expire_s}')

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
        app_log.info(f'Using cached content for {string_base}; ttl {ttl}')
    else:
        if string_base == 'a':
            ttl = 60 * 60 * 24 * 365 * 15
            r.set(string_base, 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', ex=ttl)

        spell = Speller()
        res = spell(string_base)

        if res != string_base:
            corrected = True
            ttl = 60 * 60 * 24
            r.set(string_base, res, ex=ttl)
            app_log.info(f'Cached {string_base} query with TTL at {ttl}')

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

    try:
        page = int(data.get('page'))
    except:
        page = 0

    cache = False
    res = None
    ttl = 0

    query_trimmed = query.replace(' ', '_').replace('\'', '-')
    escaped_query = f'search_{re.escape(query_trimmed)}_{page}'.lower()

    cached_result = r.get(escaped_query)
    if cached_result:
        res = json.loads(cached_result)
        cache = True
        ttl = r.ttl(escaped_query)
        app_log.info(f'Using cached result for {escaped_query}; ttl {ttl}')
    else:
        matched_content = []

        first_pass = db.Search().select().where(db.Search.title.contains(query)).paginate(page, 150)
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
            second_pass = db.Search().select().where(db.Search.title.contains(shard)).paginate(page, 150)

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

            third_pass = db.Search().select().where(db.Search.url.contains(shard)).paginate(page, 150)
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

            fourth_pass = db.Search().select().where(db.Search.description.contains(shard)).paginate(page, 150)
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
                fifth_pass = db.Search().select().where(db.Search.url.contains(shard)).paginate(page, 150)
                for content in fifth_pass:
                    match = {
                        'title': content.title,
                        'url': content.url,
                        'description': content.description
                    }

        ttl = 60 * 15
        r.set(escaped_query, str(json.dumps(matched_content)), ex=ttl)
        app_log.info(f'Cached {escaped_query} query with TTL at {ttl}')

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

    app_log.warning(f'{get_remote_ip()} added a new token {new_token} with expiry {expiry}')

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

    app_log.warning(f'{get_remote_ip()} requested a full archive')

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

    err = []
    data = request.json

    if not data:
        err.append("missing request data")

    if not err:
        token = data.get('token')
    if not err and not token or err:
        err.append("missing token")

    try:
        current_token = db.Token.select().where(db.Token.token == token).get()

        if not err and current_token.expiry_date < datetime.datetime.now():
            err.append("token has expired, please request another one")
    except:
        pass

    url, title, description = None, None, None
    if not err:
        url = data.get('url')
        title = data.get('title')
        description = data.get('description')

    if not err and not url or not title:
        err.append("invalid request")

    if not err:
        if not description:
            description = 'No description provided for this website.'

        try:
            existing_url = db.Search.select().where(db.Search.url == url).get()
        except:
            existing_url = None

        last_fetched = datetime.datetime.now()

        if existing_url:

            if existing_url.description == description and existing_url.title == title:
                app_log.info(f'{url} has already been added on {existing_url.last_fetched}')
                return jsonify({'err': 'already exists', 'fetched_on': existing_url.last_fetched})
            else:
                if existing_url.description != description:
                    existing_url.description = description

                if existing_url.title != title:
                    existing_url.title = title

                existing_url.last_fetched = last_fetched
                existing_url.save()
        else:
            new_result = db.Search(
                url=url,
                title=title,
                description=description,
                last_fetched=last_fetched
            )

            new_result.save()

        app_log.info(f'{get_remote_ip()} (using {token}) added a new URL {url} - {last_fetched}')

        return jsonify({'success': 'ok'})
    else:
        return jsonify({'err': json.dumps(err)}), 400

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
        app_log.info(f'Using cached result for {escaped_query}; ttl {ttl}')
    else:
        ddg_api_query_url = f"https://api.duckduckgo.com/?q={query}&format=json"

        req = requests.get(ddg_api_query_url)

        if req:
            response = req.json()

            res = response

            ttl = 60 * 60
            r.set(escaped_query, str(json.dumps(response)), ex=ttl)
            app_log.info(f'Cached {escaped_query} query with TTL at {ttl}')
        else:
            res = None
            ttl = -1

    return jsonify({'res': res, 'cache-hit': cache, 'ttl': ttl})

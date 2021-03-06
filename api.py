#!/usr/bin/env python3                                                                                                                        
# Author: Sergey Papyan                                                                                                                      
                                                                                                                                             
import sqlite3                                                                                                                               
from sys import argv, exit
from flask import Flask, request, jsonify, g

dbfile = 'blog.db'

app = Flask(__name__)


def get_db():
    """Open a new DB connection if there is none yet for current context"""
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(dbfile)
    return g.db


@app.teardown_appcontext
def close_db(error):
    """Close the DB connection at the end of the request"""
    if hasattr(g, 'db'):
        g.db.close()


@app.errorhandler(404)
def not_found(error):
    """General handler for unknown urls. Explicit ones may override"""
    return jsonify(
        {'error': 'invalid url',
         'available urls': [{'/post': 'method \'POST\'', '/posts': 'method \'GET\''}]}
        ), 404


@app.route('/posts', methods=['GET'])
def get_posts():
    """Handler for GET requests"""
    # Check the sanity of GET requests. 400 Bad request
    if request.values or request.data:
        return jsonify({'error': 'a GET request shouldn\'t contain query strings or body'}), 400
    # Get the db
    con = get_db()
    cur = con.cursor()
    # Query the db
    query = cur.execute('SELECT * FROM posts')
    # Parse and jsonify the results
    response = jsonify({'posts': [{'id': x[0],
        'title': x[1], 'body': x[2]} for x in query.fetchall()]})
    return response, 200


@app.route('/post', methods=['POST'])
def add_post():
    """Handler for POST requests"""
    # Check the sanity of POST requests. 400 Bad request
    if request.is_json and len(request.get_json()) == 2 and 'title' in request.get_json() and 'body' in request.get_json():
        # Get the DB
        con = get_db()
        cur = con.cursor()
        # Do the insert
        cur.execute('INSERT INTO posts(title, body) VALUES(?, ?)',
                (request.get_json()['title'], request.get_json()['body']))
        # Commit the changes
        con.commit()
        return jsonify({'success': 'true'}), 200
    else:
        return jsonify(
                {'success': 'false', 'message': 'request body should contain only \'title\' and \'body\''}
                ), 400


if __name__ == '__main__':
    if(len(argv) != 2):
        print('Usage:\nblogpost_api.py <port_num>')
        exit(1)
    app.run(port=int(argv[1]))


#!/usr/bin/env python                                                                                                                        
# Author: Sergey Papyan                                                                                                                      
                                                                                                                                             
import sqlite3                                                                                                                               
from flask import Flask, request, jsonify, g

dbfile = 'blog.db'

app = Flask(__name__)


def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(dbfile)
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {'error': 'invalid url',
         'available urls': [{'/post': 'method \'POST\'', '/posts': 'method \'GET\''}]}
        ), 404

@app.route('/posts', methods=['GET'])                                                                                                        
def get_posts():                                                                                                                             
    con = get_db()                                                                                                                           
    cur = con.cursor()                                                                                                                       
    query = cur.execute('SELECT * FROM posts')                                                                                               
    response = jsonify({'posts': [{'id': x[0],                                                                                 
        'title': x[1], 'body': x[2]} for x in query.fetchall()]})
    return response


if __name__ == '__main__':
    app.run(debug=True)


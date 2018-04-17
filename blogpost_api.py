#!/usr/bin/env python                                                                                                                        
# Author: Sergey Papyan                                                                                                                      
                                                                                                                                             
import sqlite3                                                                                                                               
from flask import Flask, request, jsonify

dbfile = 'blog.db'

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {'error': 'invalid url',
         'available urls': [{'/post': 'method \'POST\'', '/posts': 'method \'GET\''}]}
        ), 404


if __name__ == '__main__':
    app.run(debug=True)


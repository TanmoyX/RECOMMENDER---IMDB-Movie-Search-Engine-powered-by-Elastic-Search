# -*- coding: utf-8 -*-

import os
import sys
    
import elasticsearch
from elasticsearch import helpers

import pandas as pd
import json
from flask import Flask, render_template, request

# Importing custom modules
import es_connector as conn
import search_query_builder as sqb

app = Flask(__name__)
es = conn.connect_elasticsearch()

# Loading the initial welcome page to the search engine
@app.route('/')
@app.route('/index')
def index():
    
    # Query to load options for genre
    load_genre_query = {
      "aggs": {
        "keys": {
          "terms": {
            "field": "genre.keyword",
            "size": 100
          }
        }
      },
      "size": 0
    }
    genre = []
    load_genre = es.search(index = "imdb_movies", body = load_genre_query)
    for item in load_genre["aggregations"]["keys"]["buckets"]:
        genre.append(item["key"])    
    
    return render_template('index.html', list_genre = genre)


@app.route("/result", methods=['GET', 'POST'])
def get_result():
    data = request.args.to_dict()
    
    search_query = sqb.build_query(data['genre'], data['movie'], data['director'], data['actor'])
    
    result = []
    search_result = es.search(index = "imdb_movies", body = search_query)["hits"]["hits"]
    for item in search_result:
        temp = []
        temp.append(item["_source"]["title"])
        temp.append(item["_source"]["year"])
        temp.append(item["_source"]["director"])
        temp.append(item["_source"]["actors"])
        temp.append(item["_source"]["avg_vote"])
        temp.append(item["_source"]["votes"])
        temp.append(item["_source"]["duration"])
        temp.append(item["_source"]["genre"])
        temp.append(item["_source"]["country"])
        temp.append(item["_source"]["language"])
        result.append(temp)
    
    print(result)    
    
    return json.dumps({'status': 'OK', 'res': result})

if __name__ == '__main__':
    app.run()
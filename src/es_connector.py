# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch 

def connect_elasticsearch():
    es = None
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    if es.ping():
        print('Connected!')
    else:
        print('Failed to connect!')
    return es
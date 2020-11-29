# -*- coding: utf-8 -*-

from elasticsearch import helpers
import pandas as pd
import es_connector as conn

# A generator function to laod the data into our index in Elastic Search
def generator(data):
    for c, line in enumerate(data):
        yield {
            '_index' : 'imdb_movies',
            '_type'  : '_doc',
            '_id'    : c,
            '_source': {
                "title"              : line.get("title", ""),
                "original_title"     : line.get("original_title", ""),
                "year"               : line.get("year", ""),
                "genre"              : line.get("genre", ""),
                "duration"           : line.get("duration", None),
                "country"            : line.get("country", ""),
                "language"           : line.get("language", ""),
                "director"           : line.get("director", ""),
                "writer"             : line.get("writer", ""),
                "production_company" : line.get("production_company", ""),
                "actors"             : line.get("actors", ""),
                "avg_vote"           : line.get("avg_vote", None),
                "votes"              : line.get("votes", None)
            }
        }
    raise StopIteration

# Create connection object for Elastic Search
es = conn.connect_elasticsearch()

# Define our settings and mappings for the data to be inserted into the index
Settings = {
    "settings":{
        "analysis":{
            "analyzer":{
                "autocomplete":{
                    "tokenizer":"autocomplete",
                    "filter":[
                        "lowercase"
                    ]
                },
                "autocomplete_search":{
                    "tokenizer":"lowercase"
                }
            },
            "tokenizer":{
                "autocomplete":{
                    "type":"edge_ngram",
                    "min_gram":2,
                    "max_gram":20,
                    "token_chars":[
                        "letter"
                    ]
                }
            }
        }
    },
    "mappings":{
        "properties":{
            "year":{
                "type":"text"
            },
            "avg_vote":{
                "type":"float"
            },
            "title":{
                "type":"text",
                "analyzer":"autocomplete",
                "search_analyzer":"autocomplete_search"
            }
        }
    }
}
 
# Index config and creation with custom settings and mappings           
IndexName = "imdb_movies"
my = es.indices.create(index=IndexName, ignore=[400,404], body=Settings)

# Loading the data into the dataframe
df = pd.read_csv("data/IMDB-movies.csv")

# Pre-processing data
df1 = df[["imdb_title_id", "title", "original_title", "year", "genre", "duration", "country", "language", "director", "writer", "production_company", "actors", "avg_vote", "votes"]]
df1 = df1.dropna()
df1.loc[:,'genre'] = df1.genre.str.split(',').str[0]
df1.loc[:,'director'] = df1.director.str.split(',').str[0]
df1.loc[:,'language'] = df1.language.str.split(',').str[0]

# Converting the dataframe to a Python dictionary
df2 = df1.to_dict('records')

# Checking for stable connection and using the generator to load data
if es.ping():
    try:
        res = helpers.bulk(es, generator(df2))
    except StopIteration:
        print("Data upload successful!")
    except:
        print("Unknown Exception!")
else:
    print("No connection to Elastic Search!")

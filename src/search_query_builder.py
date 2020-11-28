# -*- coding: utf-8 -*-

def build_query(genre, movie, director, actor):
    if genre == "Genre" and movie == "" and director == "" and actor == "":
        # If the user did not select any parameter and simply clicks on search
        # the system will display the top rated 50 movies
        query = {
          "size": 50,
          "sort" : [
            {"avg_vote": {"order" : "desc"}}
          ]
        }
        return query
    
    query = dict()
    query["size"] = 20
#    query["sort"] = [dict()]
#    query["sort"][0]["avg_vote"] = dict()
#    query["sort"][0]["avg_vote"]["order"] = "desc"
    query["query"] = dict()
    query["query"]["bool"] = dict()
    
    if genre != "Genre":
        query["query"]["bool"]["filter"] = [dict()]
        query["query"]["bool"]["filter"][0]["term"] = dict()
        query["query"]["bool"]["filter"][0]["term"]["genre.keyword"] = genre
        
    if movie != "":
        query["query"]["bool"]["must"] = []
        if movie != "":
            query["query"]["bool"]["must"].append(dict())
            index = len(query["query"]["bool"]["must"]) - 1
            query["query"]["bool"]["must"][index]["multi_match"] = dict()
            query["query"]["bool"]["must"][index]["multi_match"]["query"] = movie
            query["query"]["bool"]["must"][index]["multi_match"]["fields"] = ["title^2", "title.edge_ng"]
            query["query"]["bool"]["must"][index]["multi_match"]["type"] = "most_fields"
    if director != "" or actor != "":
        query["query"]["bool"]["should"] = []
        if director != "":
            query["query"]["bool"]["should"].append(dict())
            index = len(query["query"]["bool"]["should"]) - 1
            query["query"]["bool"]["should"][index]["match"] = dict()
            query["query"]["bool"]["should"][index]["match"]["director"] = dict() 
            query["query"]["bool"]["should"][index]["match"]["director"]["query"] = director
            query["query"]["bool"]["should"][index]["match"]["director"]["fuzziness"] = 2
        if actor != "":
            query["query"]["bool"]["should"].append(dict())
            index = len(query["query"]["bool"]["should"]) - 1
            query["query"]["bool"]["should"][index]["match"] = dict()
            query["query"]["bool"]["should"][index]["match"]["actor"] = dict() 
            query["query"]["bool"]["should"][index]["match"]["actor"]["query"] = actor
            query["query"]["bool"]["should"][index]["match"]["actor"]["fuzziness"] = 2    
    return query
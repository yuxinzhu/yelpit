from bs4 import BeautifulSoup
import cities
import nltk
import operator
import json

import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

DEFAULT_CITY = "San Francisco"

MIN_THRESHOLD = 10
QUERY_ALL = True

# wow this is almost as page rank as Google's
PAGE_RANK = [
    ("title", 3), 
    ("h1", 3),
    ("h2", 2),
    ("h3", 2),
    ("h4", 2),
    ("b", 2),
    ("h5", 1),
    ("h6", 1),
    ("p", 1),
    ("a", 1)
    # ("div", 1)
]

PROXIMITY_MAX_RANK = 5
PROXIMITY_MAX_DEPTH = 3

def find_location(html, context, cache_key):
    html = BeautifulSoup(html)
    city_ranker = rank_city_names(html, context, cache_key)
    if city_ranker:
        return max(city_ranker.iteritems(), key=operator.itemgetter(1))[0]
    return {"San Francisco": 1000000}


def rank_city_names(html, context, cache_key):
    """
    general heuristic: takes chunks of html from <h1> to <p> and parses it
    for named entities (NE) <-- lol hope this works

    note: should also rank inside-out instead of top down using lxml tree

    """
    ranker = {}
    kill = False
    try:

        cache_hit = r.get(cache_key)
        if cache_hit:
            print 'HIT THE CACHE %s:%s' % (str(cache_key), str(cache_hit))
            ranker = json.loads(cache_hit)
        else:
            for tag, addition in PAGE_RANK:
                if not kill:
                    for element in html.find_all(tag):
                        if element.string:
                            for city in _find_city_name(element.string):
                                if _update_ranker(ranker, city, addition) >= MIN_THRESHOLD:
                                    kill = True
            print "ranker caching %s" % json.dumps(ranker)
            r.set(cache_key, json.dumps(ranker))
    except Exception as e:
        print e


    # extra credit for cities appearing in context
    for city in _find_city_name(context):
        print "getting extra credit for: %s" % str(city)
        _update_ranker(ranker, city, 5)
    # search outwardly
    return ranker

def _update_ranker(ranker, value, addition):
    if value in ranker:
        ranker[value] += addition
        return ranker[value]
    else:
        ranker[value] = addition
        return ranker[value]

def _find_named_entities(query):
    try:
        named_entities = []
        tokens = nltk.word_tokenize(query)
        pos_tags = nltk.pos_tag(tokens)
        chunks = nltk.ne_chunk(pos_tags, binary=True)
        for subtree in chunks.subtrees(filter=lambda t: t.node == "NE"):
            named_entities.append(" ".join([word for word, pos in subtree.leaves()]))
        return named_entities
    except Exception as e:
        print e
        return []

def _world_cities(named_entities):
    definitive_results = []
    for ne in named_entities:
        if ne.title() in cities.world_cities:
            definitive_results.append(ne)
    return definitive_results

def _find_city_name(query):
    ne = _find_named_entities(query)
    if ne:
        return _world_cities(ne)
    return []

def parse_business(html):
    try:
        query = html
    except Exception as e:
        print "BeautifulSoup can not parse %s --> %s" % html
    try:
        tokens = nltk.word_tokenize(query)
        pos_tags = nltk.pos_tag(tokens)
        print pos_tags
        if QUERY_ALL or True in [True for word, pos in pos_tags if pos == "NNP"]:
            print "returning business: %s" % query
            return "business", query
        print "returning subject: %s" % query
        return "subject", query
    except Exception as e:
        print "parse_business: %s" % str(e)
        return 

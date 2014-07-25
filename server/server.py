from flask import Flask, jsonify, request

import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2
import nltk

BODY = 'body'
TARGET = 'target'
RESULT = 'result'

CONSUMER_KEY = "SPJ-oX5isiNEsdCwwajTOA"
CONSUMER_SECRET = "qo3eXCuN6fFLp1djXPJrNOYFQSQ"
TOKEN = "UIhOx5m-ctCYWEggfmM5_ZlQX9nVwiZY"
TOKEN_SECRET = "sDhlx0-ZVVIGXmb1xbXRPcvkBrI"

API_HOST = 'api.yelp.com'
SEARCH_LIMIT = 1

SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

app = Flask(__name__, static_url_path='')

@app.route("/rating", methods=['POST'])
def hello():
    try:
        print request.form
        body, target = request.form[BODY], request.form[TARGET]
        print body, target

        response = search(_get_business(target), _get_location(body))
        top_business = response['businesses'][0]
        return jsonify({RESULT: top_business})
    except Exception as e:
        print e
        return jsonify({})


def yelp(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    try:
        url_params = url_params or {}
        encoded_params = urllib.urlencode(url_params)

        url = 'http://{0}{1}?{2}'.format(host, path, encoded_params)
        print url
        consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        oauth_request = oauth2.Request('GET', url, {})
        oauth_request.update(
            {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': TOKEN,
                'oauth_consumer_key': CONSUMER_KEY
            }
        )
        token = oauth2.Token(TOKEN, TOKEN_SECRET)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()

        print 'Querying {0} ...'.format(url)

        conn = urllib2.urlopen(signed_url, None)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()
        return response

    except Exception as e:
        print e

    


def search(term, location):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    url_params = {
        'term': term,
        'location': location,
        'limit': SEARCH_LIMIT
    }

    return yelp(API_HOST, SEARCH_PATH, url_params=url_params)


def _get_location(text):
  """
  returns a location from a given sample of text

  """
  return "San Francisco"

def _get_business(text):
  """
  returns the approximate name of a business given sample of text

  """
  return "Gary Danko"

def _parse_html_tree(html):
    """
    general heuristic: takes chunks of html from <h1> to <p> and parses it
    for named entities (NE) <-- lol hope this works

    """
    pass
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


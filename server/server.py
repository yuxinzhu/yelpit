from flask import Flask, jsonify, request

import argparse
import json
import pprint
import sys
import urllib
import urllib2
import oauth2
from unidecode import unidecode

import nlp

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
        # both of these are html elements
        body, target = request.form[BODY], request.form[TARGET]
        query_type, query = _get_business(target)

        num_results = 1 if query_type == "business" else 3
        response = search(query, _get_location(body), num_results)
        top_business = response['businesses'][0]
        return jsonify({RESULT: top_business})
    except Exception as e:
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
        # unicode not allowed here?
        encoded_params = urllib.urlencode(url_params)
        print encoded_params

        url = 'http://{0}{1}?{2}'.format(host, path, encoded_params)
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
        print "BLEH"
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
        print "error in request: %s" % str(e)

    
def search(term, location, num_results):
    """Query the Search API by a search term and location.

    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.

    Returns:
        dict: The JSON response from the request.
    """
    if isinstance(term, unicode):
        term = unidecode(term)
    if isinstance(location, unicode):
        location = unidecode(term)

    url_params = {
        'term': term,
        'location': location,
        'limit': num_results
    }

    return yelp(API_HOST, SEARCH_PATH, url_params=url_params)


def _get_location(html):
  """
  returns a location from a given sample of text

  """

  city = nlp.find_location(html)
  if city:
    return city
  return "San Francisco"

def _get_business(html):
  """
  returns the approximate name of a business given sample of text

  """
  return nlp.parse_business(html)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")


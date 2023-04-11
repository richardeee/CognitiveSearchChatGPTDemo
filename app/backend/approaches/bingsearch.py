# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

# You may need the below as well
# pip install pipenv
# pipenv install requests
# <importsAndVars>
import json
import os
from pprint import pprint
import requests 

'''
This sample uses the Bing Custom Search API to search for a query topic and get back user-controlled web page results.
Bing Custom Search API: https://docs.microsoft.com/en-us/bing/search-apis/bing-custom-search/overview 
'''

# Add your Bing Custom Search subscription key and endpoint to your environment variables.
subscriptionKey = "647fc23588354143a2965864ce3249d0"
endpoint = "https://api.bing.microsoft.com/v7.0/search"
# customConfigId = "679f0f8f-8abc-412f-a213-86f2716875e7"
searchTerm = "九节菖蒲与石菖蒲是同一植物吗?"
mkt = 'zh-CN'
params = { 'q': searchTerm, 'mkt': mkt }

headers = { 'Ocp-Apim-Subscription-Key': subscriptionKey }

# </importsAndVars>
# <url>
# Add your Bing Custom Search endpoint to your environment variables.
url = endpoint + "?q=" + searchTerm #+ "&customconfig=" + customConfigId
# </url>
# <request>
r = requests.get(endpoint, headers=headers, params=params)
json_response = json.loads(r.text)
# web_pages = jsonpath.jsonpath(json_response,'$..snippet')
# r = requests.get(url, headers={'Ocp-Apim-Subscription-Key': subscriptionKey})
# pprint(json.loads(r.text))
# results = [page for page in web_pages]

pprint(list(json_response['webPages']['value'])[:3])
# pprint(json_response['webPages'])
# results = [doc['WebPages'] + ": " + nonewlines(doc[self.content_field]) for doc in r]
# </request>
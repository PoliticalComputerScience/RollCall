""" This file contains get_json(api_url) which returns the dictionary form of
JSON object returned by the ProPublica API. """

from urllib.request import Request, urlopen
import json
API_KEY = "dtoa6UrIaAQBqiXOdBPmFeS36VyVxxorxqU4mXkv"

def get_json(api_url):
	if not api_url:
		return None
	query = Request(api_url)
	query.add_header("X-API-KEY", API_KEY)
	res = json.loads(urlopen(query).read().decode("utf-8"))
	if res["status"] != "OK":
		print("invalid query: " + res["status"])
		return None
	return res

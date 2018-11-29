"""
This file contains get_json(api_url) which returns the dictionary form of
JSON object returned by the ProPublica API as well as functions for writing to
and from csv files.
"""

from urllib.request import Request, urlopen
import json, csv
API_KEY = "npwl9Pn4rk2qFvIKOvzKbXH1AvM82Omi20tfyrFl"

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

""" Given header and list of tuples, writes to csv file <name>.csv """
def to_csv(header, data, name):
    with open(name,'w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(header)
        csv_out.writerows(data)

""" Reads a csv and returns a list of tuples. """
def from_csv(filename):
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data[1:] #removes header

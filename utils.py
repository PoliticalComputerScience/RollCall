"""
This file contains get_json(api_url) which returns the dictionary form of
JSON object returned by the ProPublica API as well as functions for writing to
and from csv files.
"""

from urllib.request import Request, urlopen
import json, csv, sys, re
API_KEY = "npwl9Pn4rk2qFvIKOvzKbXH1AvM82Omi20tfyrFl"
CURR_CONGRESS = 116 #Sorry, magic number. Update after January 3, 2019
CHAMBERS = ["both", "house", "senate"]

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

""" Given header and list of tuples, writes to csv file data/<filename>. """
def to_csv(header, data, filename):
    filename = "data/" + filename
    with open(filename,'w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(header)
        csv_out.writerows(data)

""" Reads a csv from data/<filename> and returns a list of tuples. """
def from_csv(filename):
    filename = "data/" + filename
    data = []
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    return data[1:] #removes header


def get_data(api_url):
    wrapper = get_json(api_url)
    return wrapper["results"]

def validate_congress(congress_num):
    if type(congress_num) != int:
        raise TypeError(str(congress_num) + " not supported, congresses must be of type int")
    if congress_num < 105 or congress_num > CURR_CONGRESS:
        raise RuntimeError(str(congress_num) + " is not a valid congress number")

def validate_slug(slug):
    if type(slug) != str:
        raise TypeError(str(slug) + " not supported, slugs must be of type str")
    pattern = "(hr|s|hres|hjres|sjres|sconres|sres|hconres)[1-9][0-9]*"
    matcher = re.compile(pattern)
    if not matcher.match(slug):
        raise RuntimeError(slug + " is not a valid slug, slugs must match " + pattern)

def format_slug(slug):
    """Converts slug in congress.gov format (H.R.302) to propublic format (hr302)"""
    return slug.replace(".", "").lower()

def validate_chamber(chamber):
    if type(chamber) != str:
        raise TypeError(str(chamber) + " not supported, chambers must be of type str")
    if chamber not in CHAMBERS:
        raise RuntimeError(chamber + " is not a valid congress number, chamber must be one of [both, house, senate]")

def ind_to_node_map(graph):
    ind = 0
    ind_to_node = {}
    for n in graph.nodes:
        ind_to_node[ind] = n
        ind += 1
    return ind_to_node




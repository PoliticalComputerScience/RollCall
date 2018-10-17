from utils import get_json
import json, csv
from datetime import date
from math import sqrt
CHAMBERS = ["both", "house", "senate"]
CURR_CONGRESS_START = "2017-01-03"

""" Converts (and filters) a list of votes into a list of URI's for the votes corresponding to bills. """
def filter_uri(votes):
    uri_list = []
    for v in votes:
        if (("bill" in v) and (v["question"] == "On Passage")):
            uri_list.append(v["vote_uri"])
    return uri_list

""" Converts a list of URI's into a list of {'bill_id':bill_id, 'positions':[pos0, pos1, ...]} corresponding to each URI. """
def uri_to_roll_call(uri_list):
    roll_calls = []
    for u in uri_list:
        r = get_json(u)["results"]["votes"]["vote"]
        d = dict()
        d['bill_id'] = r['bill']['bill_id']
        d['positions'] = r['positions']
        roll_calls.append(d)
    return roll_calls

def get_vote_info(start_date, end_date, chamber="both"):
    assert chamber in CHAMBERS, chamber + " is not an acceptable chamber"
    vote_info = get_json("https://api.propublica.org/congress/v1/" + chamber + "/votes/" + start_date + "/" + end_date + ".json")
    assert vote_info and vote_info["results"], "empty vote_info"
    return vote_info["results"]

""" Gets the roll call information for the votes in the provided time interval. The time interval must be less than 1 month. NOTE: NOT WORKING """
def get_vote_roll_call(start_date, end_date, chamber="both"):
    vote_info = get_vote_info(start_date, end_date, chamber)
    uri_list = filter_uri(vote_info["votes"])
    return uri_to_roll_call(uri_list)

def get_year_vote_info(year=2018, chamber="both"):
    assert type(year) == int and year <= 2018 and year > 1900 and chamber in CHAMBERS
    year = str(year)
    month_to_vote_info = {}
    last = 13
    if (year == 2018):
        last = int(date.today().month)
    for i in range(1, last):
        month = str(i)
        if i < 10:
            month = "0" + month
        month_vote_info = get_json("https://api.propublica.org/congress/v1/" + chamber + "/votes/" + year + "/" + month + ".json")
        month_to_vote_info[i] = month_vote_info["results"]
    return month_to_vote_info

""" Gets the roll call information for the votes in the given year. """
def get_year_vote_roll_call(year=2018, chamber="both"):
    vote_info = get_year_vote_info(year, chamber)
    uri_list = []
    for i in range(1, 13):
        uri_list += filter_uri(vote_info[i]["votes"])
    return uri_to_roll_call(uri_list)

def get_congress_vote_info(congress, chamber="both"):
    assert chamber in CHAMBERS and type(congress) == int and congress <= 115 and congress >= 1
    offset = 115 - congress
    year = 2017 - offset * 2
    congress_vote_info = {}
    congress_vote_info[1] = get_year_vote_info(year, chamber)
    congress_vote_info[2] = get_year_vote_info(year + 1, chamber)
    return congress_vote_info

""" Gets the roll call information for the votes in the given congress. """
def get_congress_vote_roll_call(congress, chamber="both"):
    offset = 115 - congress
    year = 2017 - offset * 2
    roll_call_list = get_year_vote_roll_call(year, chamber) + get_year_vote_roll_call(year + 1, chamber)
    return roll_call_list

""" Processes and stores vote roll call data (zipped together with dw_nominate scores) to file. This is to save us from having to always make API calls. """
def store_vote_data(unprocessed_data, file_name):
    member_map = extract_member_map()
    processed = zip_dw_nom(unprocessed_data, member_map)
    with open(file_name, 'w') as f:
        json.dump(processed, f)

""" Extracts processed vote data from file to be scored with polarization formula. """
def extract_processed_data(file_name):
    with open(file_name) as json_data:
        votes = json.load(json_data)
    return votes




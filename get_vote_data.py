from utils import get_json
import json, csv
from datetime import date
from math import sqrt
import pandas as pd
import itertools as it
CHAMBERS = ["both", "house", "senate"]
CURR_CONGRESS_START = "2017-01-03"

""" Converts (and filters) a list of votes into a list of URI's for the votes corresponding to bills.
    TODO: Filter out the roll calls that we care about. """
def filter_uri(votes):
    uri_list = []
    for v in votes:
        if (("bill" in v) and ("On Passage" in v["question"])):
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

""" Helper function for get_year_vote_roll_call() """
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


""" Constructs a dictionary that maps congressmembers to how they voted on certain bills"""
def get_member_votes(congress, chamber="both"):
  big_boy = get_congress_vote_roll_call(congress, chamber)
  my_dict = {}

  for tuple1 in big_boy:

    bill_ID = tuple1['bill_id']
    positions = tuple1['positions']

    for member_position in positions:

      member_id = member_position["member_id"]
      member_vote = member_position["vote_position"]

      if (member_id not in my_dict.keys()):
          my_dict[member_id] = []
      if (member_vote != "Not Voting"): #Filter out abstaining Congress members
          my_dict[member_id] += [(bill_ID, member_vote)]

  return my_dict



""" Constructs a set of all combinations of 2 members, storing:
		1) How many bills they voted the same on
		2) How many bills they both voted on
    Should call on either Senate or House, both may not be entirely useful.
"""
def pair_similarity(congress, chamber='both'):
	member_pairs = set()
	member_votes = get_member_votes(congress, chamber)

	for m in it.combinations(member_votes.keys(), 2):

		if m[0] == m[1]:
			continue
		#[(bill_id, vote), (bill_id, vote)...]
		m1 = member_votes[m[0]]
		m2 = member_votes[m[1]]

		# tables of [(bill_id, vote),(bill_id, vote) ...]
		d1 = pd.DataFrame(m1, columns=['bill_id1','vote1'])
		d2 = pd.DataFrame(m2, columns=['bill_id2','vote2'])

		d3 = d1.merge(d2, how="inner", left_on='bill_id1', right_on='bill_id2')
		vs = d3.loc[d3['vote1'] == d3['vote2'],:].shape[0]
		vt = d3.shape[0]

		ntuple = (m[0], m[1], vs, vt)
		member_pairs.add(ntuple)

	# store_as_csv(member_pairs)

	return member_pairs


# def store_as_csv(pairs)
# 	dataframee = pd.DataFrame(pairs, columns=['member_1', 'member_2', 'votes_same',''])
# 	dataframee.to_csv('Pairs')

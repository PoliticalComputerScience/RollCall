#from utils import get_json, to_csv
from utils import *
from datetime import date
from Pair import *
import pandas as pd
import itertools as it
CHAMBERS = ["both", "house", "senate"]
CURR_CONGRESS_START = "2017-01-03"

"""
    Creates and returns a dictionary with pairs of congressmembers as keys and
    their data dictionaries as values.
"""
def get_pairs(congress, chamber):
    uri = "https://api.propublica.org/congress/v1/{}/{}/members.json".format(congress, chamber)
    members = get_json(uri)['results'][0]['members']
    pairs = dict()
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            pair = Pair(members[i]['id'], members[j]['id'], \
                        members[i]['first_name'] + ' ' + members[i]['last_name'], \
                        members[j]['first_name'] + ' ' + members[j]['last_name'])
            pairs[pair] = pair.data
    return pairs

"""
    Converts (and filters) a list of votes into a list of URI's for the votes
    corresponding to bills.
    TODO: Filter out the roll calls that we care about.
"""
def filter_uri(votes):
    uri_list = []
    for v in votes:
        if (("bill" in v) and ("On Passage" in v["question"])):
            uri_list.append(v['vote_uri'])
    return uri_list

"""
    Converts a list of URI's into a list of {'bill_id':bill_id, 'positions':
    [pos0, pos1, ...]} corresponding to each URI.
"""
def uri_to_roll_call(uri_list):
    roll_calls = []
    for u in uri_list:
        r = get_json(u)["results"]["votes"]["vote"]
        d = dict()
        d['bill_id'] = r['bill']['bill_id']
        d['positions'] = r['positions']
        roll_calls.append(d)
    return roll_calls

"""
    Helper function for get_year_vote_roll_call()
"""
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

"""
    Gets the roll call information for the votes in the given year using get_year_vote_info
"""
def get_year_vote_roll_call(year=2018, chamber="both"):
    vote_info = get_year_vote_info(year, chamber)
    uri_list = []
    for i in range(1, 13):
        uri_list += filter_uri(vote_info[i]["votes"])
    return uri_to_roll_call(uri_list)

"""
    Gets the roll call and sponsorship information for the votes in the given congress.
    Returns of list of dictionarys {'bill_id': bill_id, 'positions': positions, 'sponsor_list': sponsor_list}
"""
def get_congress_vote_roll_call(congress, chamber="both"):
    offset = 115 - congress
    year = 2017 - offset * 2
    roll_call_list = get_year_vote_roll_call(year, chamber) + get_year_vote_roll_call(year + 1, chamber)
    roll_call_sponsors = []
    for roll_call in roll_call_list:
        bill_id = roll_call['bill_id']
        sponsors_uri = 'https://api.propublica.org/congress/v1/' + str(congress) + '/bills/' + bill_id.split('-')[0] + '/cosponsors.json'
        bill = get_json(sponsors_uri)
        if bill:
            sponsor_list = [bill['results'][0]['sponsor_id']]
            for cosponsor in bill['results'][0]['cosponsors']:
                sponsor_list.append(cosponsor['cosponsor_id'])
            roll_call['sponsor_list'] = sponsor_list
    return roll_call_list


"""
    Constructs a dictionary that maps congressmembers to how they voted on certain bills
    @Param
"""
def get_member_votes(big_boy):

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


"""
    Constructs a set of all combinations of 2 members, storing:
        1) How many bills they voted the same on
        2) How many bills they both voted on
    Should call on either Senate or House, both may not be entirely useful.
    Returns a list of tuples (member0, member1, votes_same, bills_same)
"""
def pair_similarity(member_votes, pairs):#congress, chamber='both'):

    for m in it.combinations(member_votes.keys(), 2):

        if m[0] == m[1]:
            continue

        m1 = member_votes[m[0]]
        m2 = member_votes[m[1]]

        d1 = pd.DataFrame(m1, columns=['bill_id1','vote1'])
        d2 = pd.DataFrame(m2, columns=['bill_id2','vote2'])

        d3 = d1.merge(d2, how="inner", left_on='bill_id1', right_on='bill_id2')
        vs = d3.loc[d3['vote1'] == d3['vote2'],:].shape[0]
        vt = d3.shape[0]

        dummy_pair = Pair(m[0], m[1]) #used to access dictionary
        try:
            pairs[dummy_pair]['votes_same'] = vs
            pairs[dummy_pair]['votes_total'] = vt
        except KeyError:
            print("Discrepancy in ProPublica member data")


"""
Aggregates pairs for the congress and chamber, writing data to the file
<congress>_<chamber>.csv
"""
def write_pairs(congress, chamber='both'):
    pairs = get_pairs(congress, chamber) #creates dictionary mapping pair hashes to pairs
    roll_calls = get_congress_vote_roll_call(congress, chamber)
    member_votes = get_member_votes(roll_calls)
    pair_similarity(member_votes, pairs)#congress, chamber)
    #adding mutual sponsorship data to pair data dictionaries
    for pair in pairs.keys():
        for roll_call in roll_calls:
            if (pair.id_a in roll_call['sponsor_list'] and \
            pair.id_b in roll_call['sponsor_list']):
                pair.data['mutual_sponsorships'] += 1
    #You can do further processing to the pairs here

    new_pairs = [k.toTuple() for k in pairs.keys()]
    to_csv(['member_a_id', 'member_b_id', 'member_a_name', 'member_b_name', \
        'votes_same', 'bills_same', 'mutual_sponsorships'], new_pairs, \
        str(congress) + '_' + chamber + '.csv')
"""
if __name__ == "__main__":
    sessions = [109]
    for session in sessions:
        print('Session: ' + str(session))
        try:
            write_pairs(session, 'senate')
        except KeyError:
            print("key error")
"""

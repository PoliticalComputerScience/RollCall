from utils import get_json
import json, csv
from datetime import date
from Member import Member
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

""" Converts a list of URI's into a list of the roll call information for the vote corresponding to each URI. """
def uri_to_roll_call(uri_list):
    roll_calls = []
    for u in uri_list:
        r = get_json(u)["results"]["votes"]["vote"]
        roll_calls.append(r)
    return prune(roll_calls)

""" Prunes unnecessary data from each vote in the list of roll_calls. """
def prune(roll_calls):
    for r in roll_calls:
        r.pop("session", None)
        r.pop("source", None)
        r.pop("url", None)
        r.pop("time", None)
        r.pop("document_number", None)
        r.pop("document_title", None)
        r.pop("tie_breaker", None)
        r.pop("tie_breaker_vote", None)
        r.pop("vote_type", None)
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

def get_curr_vote_info(chamber="both"):
    return get_vote_info(CURR_CONGRESS_START, date.today().isoformat(), chamber)

""" Gets the roll call information for the votes in the current congressional session. NOTE: NOT WORKING """
def get_curr_vote_roll_call(chamber="both"):
    return uri_to_roll_call(get_vote_uri(CURR_CONGRESS_START, date.today().isoformat(), chamber))

def get_recent_vote_info(chamber="both"):
    assert chamber in CHAMBERS
    recent_vote_info = get_json("https://api.propublica.org/congress/v1/"+ chamber + "/votes/recent.json")
    return recent_vote_info["results"]

""" Gets the roll call information for the 20 most recent votes. """
def get_recent_vote_roll_call(chamber="both"):
    vote_info = get_recent_vote_info(chamber)
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

def process_congress_vote_info(cong_vi):
    ret = []
    for year in cong_vi:
        year_dict = cong_vi[year]
        for month in range(1, 13):
            month_dict = year_dict[month]
            month_rcb = get_roll_calls_and_bills(month_dict)
            ret.append(month_rcb)
    return ret
	
def get_roll_calls_and_bills(vote_info):
    votes = vote_info["results"]["votes"]
    ret = []
    for vote in votes:
        vote_link, bill_link = get_vote_link(vote), get_bill_link(vote)
        ret.append((get_json(vote_link), get_json(bill_link)))
    return ret

def get_bill_link(vote):
    try:
        bill_link = vote["bill"]["api_uri"]
    except KeyError:
        bill_link = ""
    return bill_link

def get_vote_link(vote):
    try: 
        vote_link = vote["vote_uri"]
    except KeyError:
        vote_link = ""
    return vote_link

def extract_member_map(file="members.csv"):
    f = open(file, "r")
    csv_reader = csv.DictReader(f)
    member_map = {}
    for row in csv_reader:
        bioguide_id = row["bioguide_id"]
        if (row["bioname"] and row["nominate_dim1"] and row["nominate_dim2"]):
            member_map[bioguide_id] = Member(bio_id=bioguide_id, name=row["bioname"], dw_1=float(row["nominate_dim1"]), dw_2=float(row["nominate_dim2"]))
    f.close()
    return member_map

""" Zips the real DW_nominate data into the vote roll call data. """
def zip_dw_nom(roll_calls, member_map):
    for vote in roll_calls:
        to_remove = []
        for p in vote["positions"]:
            member_id = p["member_id"]
            p.pop("dw_nominate")
            if (member_id not in member_map): #no dw_nominate or bioguide_id
                to_remove.append(p)
            else:
                p["dw_dim1"] = member_map[member_id].dw_1
                p["dw_dim2"] = member_map[member_id].dw_2
        for p in to_remove:
            vote["positions"].remove(p)
    return roll_calls

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

""" For each bill in the list of votes, assigns polarization scores on each axis and stores the result in a csv with the header [bill_number, bill_id, api_uri, p1, p2]. """
def score_those_bills(votes, file_name, scale_factor=1):    
    
    bills = []
    for vote in votes:
        
        bill = {}
        bill['bill_number'] = vote['bill']['number']
        bill['bill_id'] = vote['bill']['bill_id']
        bill['api_uri'] = vote['bill']['api_uri']
        c1 = [0, 0] #[sum_yea_dw_nominate, sum_nay_dw_nominate]
        c2 = [0, 0] # for axis 2 of the polarization scores
        num_yea = 0
        num_nay = 0
        positions = vote['positions']
        for p in positions:
            dw1 = p['dw_dim1']
            dw2 = p['dw_dim2']           
            if (p['vote_position'] == "Yes"):
                num_yea += 1
                c1[0] += dw1
                c2[0] += dw2
            elif (p['vote_position'] == "No"):
                num_nay += 1
                c1[1] += dw1
                c2[1] += dw2
        num_votes = num_yea + num_nay
        p1 = (c1[0] - c1[1]) / num_votes
        p2 = (c2[0] - c2[1]) / num_votes
        bill['p1'] = p1 * scale_factor
        bill['p2'] = p2 * scale_factor
        bills.append(bill)
    keys = bills[0].keys()
    with open(file_name, "w") as f:
        csvWriter = csv.DictWriter(f, keys)
        csvWriter.writeheader()
        csvWriter.writerows(bills)

#HELPER that calculates influence of a certain rep's vote on the bill score
def quick_maths(score1, score2, party, yes, bill_dw1, bill_dw2):
    # Again, not sure how party is represented
    if (yes and party == 'Republican') or (not yes and party == 'Democrat'):
        bill_dw1 += abs(score1)
        bill_dw2 += abs(score2)
    if (yes and party == 'Democrat') or (not yes and party == 'Republican'):
        bill_dw1 -= abs(score1)
        bill_dw2 -= abs(score2)
    return [bill_dw1, bill_dw2]

#HELPER that nomalizes bills scores
def normalize(score, bill_dw_1, bill_dw_2):
    return score / sqrt(bill_dw_1**2 + bill_dw_2**2)











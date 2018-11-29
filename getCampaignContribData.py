from crpapi import CRP, CRPApiError
import xml.etree.ElementTree as ET
import json

CRP.apikey = '3b04c85484ca2ecbcb14c9617f8b26aa'
state_names = ["AL", "AK", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK" , "OR", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]


"""This function produces a map from official congressional IDS to CRPs IDs for all congressman in a given session"""

"""Unfortunately, since this API does not support retrieving data from previous sessions of congress,
it has no input variable."""

def gen_cand_lst():
    official_IDs = []
    CRP_IDs = []
    big_dict = {}

    for state in state_names:
        """api call"""
            dict = json.load(CRP.getLegislators(CRP.apikey, state, "json"))
            for leg in dict.keys():
                big_dict[dict["bioguide_id"]] = [dict["cid"]]
    return big_dict


"""Given the congressional ID of a candidate, this function returns a map from industry name to total amount of
money accepted from that industry. Both are strings. """
def get_contribs_by_industry(id):
    returned = {}
    tree = ET.parse(CRP.candIndustry(CRP.apikey, state, "json"))
    for child in tree:
        dict = child.attrib
        returned[dict["industry_name"]] = dict["total"]
    return returned

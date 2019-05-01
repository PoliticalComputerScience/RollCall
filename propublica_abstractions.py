# A file that will contain all code used to make propublica requests.

from utils import get_json, validate_congress, validate_slug, validate_chamber, get_data
import json, csv, re
from functools import lru_cache



class Member:
    """
    a class to represent a congressional member
    """
    def __init__(self, _id, name, party, state):
        self._id = _id
        self.name = name
        self.party = party
        self.state = state

class Endpoint:
    """
    a pseudo-abstract class to represent a general ProPublica API endpoint

    Instances of this class should never be created, only instances of child classes (Bill, RollCall)
    """
    def __init__(self, api_url="", json_data={}):
        """
        creates a new Endpoint Object

        @param api_url: (type=str) a url that points to a ProPublica Endpoint
        @param json_data: (type=dict)
        """
        assert api_url or json_data
        if json_data:
            self.data = json_data
        else:
            self.data = get_data(api_url) #this data field should never be accessed directly

class Bill(Endpoint):

    def __init__(self, api_url="", json_data={}, congress=0, slug=""):
        """creates a new Endpoint Object

        @param api_url: (type=str) a url that points to a ProPublica Endpoint
        @param json_data: (type=dict)
        @param congress: (type=int) index of the congress the bill was introduced in
        @param slug: (type=str) identifier for bill, see utils.validate_slug for format
        """
        assert api_url or json_data or (congress and slug)
        if json_data or api_url:
            super().__init__(api_url=api_url, json_data=json_data)
        else:
            validate_congress(congress)
            validate_slug(slug)
            url = "https://api.propublica.org/congress/v1/" + str(congress) +"/bills/"+ slug + ".json"
            super().__init__(api_url=url)
        if type(self.data) == list:
            self.data = self.data[0] #trust me, propublica sucks
        self.cached_cosponsors = False
        self.cached_subjects = False
        self.cosponsors = []
        self.subjects = []

    def __repr__(self):
        short_title = self.get_title()
        #chars_allowed = 72
        #if len(short_title) > chars_allowed:
        #    short_title = short_title[:chars_allowed-2] + "..."
        return "<Bill slug: {}, subject: {}, congress num: {}, title: {}>".format(self.get_slug(), self.get_subject(), self.get_congress(), short_title)

    def __eq__(self, other):
        return self.slug == other.slug and self.congress == other.congress

    def get_subject(self):
        """
        returns the subject tag of this bill (type=str)
        """
        return self.data["primary_subject"]

    def get_slug(self):
        """
        returns the slug of this bill (type=str)
        """
        return self.data["bill_slug"]

    def get_congress(self):
        """
        returns the congress of this bill (type=int)
        """
        # this *should* be what we use, but not all queries include this for some reason
        #return int(self.data["congress"])
        return int(self.data["bill_id"].split("-")[1])

    def get_title(self):
        """
        returns the title of this bill (type=str)
        """
        return self.data["title"]

    def get_sponsor(self):
        """
        returns the sponsor of this bill, represented as a tuple (<id>, <name>, <url>),
        (type=tuple<str>)
        """
        return Member(_id=self.data["sponsor_id"], name=self.data["sponsor"],
        party=self.data["sponsor_party"], state=self.data["sponsor_state"])

    def get_cosponsors(self):
        """
        returns a list of the cosponsors for this bill
        """
        if self.cached_cosponsors:
            return self.cosponsors
        slug, congress = self.get_slug(), self.get_congress()
        api_url = "https://api.propublica.org/congress/v1/"+ str(congress) + "/bills/" + slug + "/cosponsors.json"
        data = get_data(api_url)[0]
        cosponsors = []
        for cosponsor_dict in data["cosponsors"]:
            cosponsor = Member(_id=cosponsor_dict["cosponsor_id"], name=cosponsor_dict["name"], party=cosponsor_dict["cosponsor_party"], state=cosponsor_dict["cosponsor_state"])
            cosponsors.append(cosponsor)
        self.cosponsors = list(cosponsors)
        self.cached_cosponsors = True
        return cosponsors

    def get_recent_bills(congress=115, chamber="both", action="introduced"):
        """
        returns objects for the 20 most recent bills to have undergone <action> in <chamber> of <congress>

        @param congress: (type=int) index of congress (needs to be between 105, 115
        @param action: (type=str) a string representing the type of action to be used for lookup,
        action must be one of [introduced, updated, active, passed, enacted, vetoed]
        @return: (type=list<Bill>) a list of the 20 most recently <action>'d bill objects
        """
        chamber = chamber.replace(" ","").lower()
        action = action.replace(" ","").lower()
        validate_congress(115)
        validate_chamber(chamber)
        if action not in ["introduced", "updated", "active", "passed", "enacted", "vetoed"]:
            raise ValueError(str(action) + "is not a valid action")
        data = get_data("https://api.propublica.org/congress/v1/" + str(congress) + "/" + chamber + "/bills/" + action + ".json")
        bills = data[0]["bills"]
        return [Bill(json_data=bill_dict) for bill_dict in bills]

    #@lru_cache()
    #Bills aren't hashable oops
    def get_subjects(self):
        if self.cached_subjects:
            return self.subjects
        data = get_data('https://api.propublica.org/congress/v1/{congress}/bills/{slug}/subjects.json'.format(
            congress=self.get_congress(),
            slug=self.get_slug(),
        ))
        assert data[0]['bill_id'] == self.data['bill_id']
        ret = data[0]['subjects']
        self.cached_subjects = True
        self.subjects = ret
        return ret

class Vote(Endpoint):
    


if __name__ == '__main__':
    bills = Bill.get_recent_bills(action='passed')
    for bill in bills:
        print(bill)

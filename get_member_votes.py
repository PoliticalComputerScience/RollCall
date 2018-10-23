
def get_member_votes(congress, chamber = "both"):
  big_boy = get_congress_vote_roll_call(congress, chamber)
  my_dict = {}

  for tuple1 in big_boy:

    bill_ID = tuple1['bill_id']
    positions = tuple1['positions']

    for member_position in positions:

      member_id = member_position["member_id"]
      member_vote = member_position["vote_position"]

      """if (member_id not in my_dict.keys()):
          my_dict[member_id] = []
      if (member_vote != "Not Voting"): #Filter out abstains
          my_dict[member_id] += [(bill_ID, member_vote)]"""

      if (member_id in my_dict.keys()):
          my_dict[member_id] += [(bill_ID, member_vote)]
      else:
        my_dict[member_id] = []
        my_dict[member_id] += [(bill_ID, member_vote)]

  return my_dict

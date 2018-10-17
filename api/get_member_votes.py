
def get_member_votes(congress, chamber = "both"):
  big_boy = get_congress_vote_roll_call(congress, chamber)
  my_dict = {}
  for tuple in big_boy:
    bill_ID = tuple['bill_id']
    positions = tuple['positions']
    for member_position in positions:
      member_id = member_position["member_id"]
      member_vote = member_position["vote_position"]
      if (member_id in big_boy):
        if (member_vote == "Yes"):
          my_dict[member_id] += [(bill_ID, "Yes")]
        else if (member_vote == "No"):
          my_dict[member_id] += [(bill_ID, "No")]
      else:
        my_dict[member_id] = []
        if (member_vote == "Yes"):
          my_dict[member_id] += [(bill_ID, "Yes")]
        else if (member_vote == "No"):
          my_dict[member_id] += [(bill_ID, "No")]
  return my_dict

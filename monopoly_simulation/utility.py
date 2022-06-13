def trade():
    pass

def auction(participants, minimum_bid):
    max = minimum_bid
    bid_list = []
    for i in range(len(participants)):
        bid = participants[i].place_bid()
        if bid <= max:
            participants.remove(i)
        else:
            bid_list[i] = bid

    if len(participants) == 1:
        return participants[0]
    else:
        return auction(participants=participants, minimum_bid=max)
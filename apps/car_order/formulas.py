MIN_TRANSPORT_TO_INCLUDE = 6000


def get_transport(transport):
    return transport * (transport > MIN_TRANSPORT_TO_INCLUDE)


def calculate_total(price, auctionFees, recycle, transport):
    included = (price, price * 0.1, auctionFees, recycle, transport)
    return sum(included)


def calculate_total_fob(price, amount, transport, fob):
    transport = get_transport(transport)

    included = (price, amount, transport, fob)
    return sum(included)


def calculate_total_fob2(price, auctionFees, transport, fob):
    included = (price, auctionFees, get_transport(transport), fob)
    return sum(included)

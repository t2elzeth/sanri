MIN_TRANSPORT_TO_INCLUDE = 6000


def get_transport(transport, limit):
    return transport * (transport > limit)


def calculate_total(price, auctionFees, recycle, transport):
    included = (price, price * 0.1, auctionFees, recycle, transport)
    return sum(included)


def calculate_total_fob(price, amount, transport, fob, transportation_limit):
    transport = get_transport(transport, transportation_limit)

    included = (price, amount, transport, fob)
    return sum(included)


def calculate_total_fob2(
    price, auctionFees, transport, fob, transportation_limit
):
    included = (
        price,
        auctionFees,
        get_transport(transport, transportation_limit),
        fob,
    )
    return sum(included)

def calculate_total(price, recycle, auctionFees, salesFees):
    include_sum = (price, price * 0.1, recycle)
    include_sub = (auctionFees, salesFees)
    return sum(include_sum) - sum(include_sub)

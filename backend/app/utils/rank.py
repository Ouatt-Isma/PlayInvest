ADDING_FACTOR = 1000

def adjusted_rank(rank, total_portfolios):
    """
    Inflates ranks in the lower half of the leaderboard by ADDING_FACTOR.
    total_portfolios is the raw DB count (without the factor added).
    """
    if rank is None:
        return None
    total_users = total_portfolios + ADDING_FACTOR
    if rank < (total_users - ADDING_FACTOR) / 2:
        return rank
    return rank + ADDING_FACTOR

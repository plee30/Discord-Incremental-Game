# Building costs

# Lumber Mill Costs
# Formula is ROUND((10 * (1.5^(level-1))))
def lumber_mill_cost(level):
    return int(10 * (1.5 ** (level-1)))

# Lumber Mill Generation
# Formula is ROUND(2*2^(level/5))
def lumber_mill_generates(level):
    return int(2 * 2 ** (level/5))
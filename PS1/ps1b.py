###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight_greedy(egg_weights, target_weight, memo = {}):
    #this is the greedy algorithm. optimal solution imo, but is not dynamic programming
    total = 0
    calls = 0
    for eggs in egg_weights:
        memo[eggs] = 0
    for egg in reversed (egg_weights):
        
        while total < target_weight:
            calls+=1
            if (total + egg) > target_weight:
                break
            memo[egg] = memo.get(egg,0)+1
            total+= egg
    print("# calls", calls)
    return sum(memo.values())

def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """

#this is dynamic programming, my iterative approach
    store = set()
    calls = 0
    for i in range (len(egg_weights),0,-1):
        rem_weight = 0
        egg_weights_copy = egg_weights
        result_tup = ()
        nextVal = egg_weights[i-1]
        while rem_weight < target_weight:
            calls+=1
            while nextVal+rem_weight > target_weight: 
                egg_weights_copy = egg_weights_copy[:-1]
                nextVal = egg_weights_copy[-1]
            if (len(egg_weights_copy),rem_weight) in memo:
                nextVal = memo[(len(egg_weights_copy),rem_weight)]
#                    print("memo used", nextVal)
            result_tup += (nextVal,)
            rem_weight+=nextVal
            memo[(len(egg_weights_copy),rem_weight)] = nextVal
            
#            print("result tup", result_tup)
        store.add(len(result_tup))
    print("# calls", calls)
    return min(store)

#this is dynamic programming. from github
#    minEggs = target_weight
#    if target_weight in egg_weights:
#        memo[target_weight] = 1
#        return 1
#    elif memo[target_weight] > 0:
#        return memo[target_weight]
#    else:
#        for i in [c for c in egg_weights if c <= target_weight]:
#            numEggs = 1 + dp_make_weight(egg_weights, target_weight - i, memo)
#            if numEggs < minEggs:
#                minEggs = numEggs
#                memo[target_weight] = minEggs
#    return minEggs
    
# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10,11,12,13,16,19, 25)
    n =2134
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
#    print("Actual output:", dp_make_weight(egg_weights, n,memo = [0]*(n + 1)))#for the github approach
    print("Actual output:", dp_make_weight_greedy(egg_weights, n))#for my greedy approach
    print("Actual output:", dp_make_weight(egg_weights, n))#for my dp approach


    print()
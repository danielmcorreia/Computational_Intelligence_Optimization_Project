from random import randint, sample

def swap_mutation(individual):
    
    '''swaps 2 random point genes directly within the individual'''
    
    #chooses a row of the individual to perform the mutation on, randomly
    random_row = randint(0, len(individual)-1)
    # Get two mutation points
    mut_points = sample(range(len(individual[random_row])), 2)
    individual[random_row][mut_points[0]], individual[random_row][mut_points[1]] = individual[random_row][mut_points[1]], individual[random_row][mut_points[0]]
    
    return individual


def inversion_mutation(individual):
    
    '''inverts 2 random strings of genes within individual'''
    
    #chooses a row of the individual to perform the mutation on, randomly
    random_row = randint(0, len(individual)-1)
    # Position of the start and end of substring
    mut_points = sample(range(len(individual[random_row])), 2)
    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    # Invert for the mutation
    individual[random_row][mut_points[0]:mut_points[1]] = individual[random_row][mut_points[0]:mut_points[1]][::-1]

    return individual


def scramble_mutation(individual):
    
    '''shuffles 2 random strings of genes within individual'''
    
    #chooses a row of the individual to perform the mutation on, randomly
    random_row = randint(0, len(individual)-1)
    # Position of the start and end of substring
    mut_points = sample(range(len(individual[random_row])), 2)
    # This method assumes that the second point is after (on the right of) the first one
    # Sort the list
    mut_points.sort()
    # shuffles segment to be sorted and replaces it in in individual
    individual[random_row][mut_points[0]:mut_points[1]] = sample(individual[random_row][mut_points[0]:mut_points[1]], len(range(mut_points[0], mut_points[1])))

    return individual
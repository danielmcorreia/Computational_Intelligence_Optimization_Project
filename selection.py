from random import uniform, sample
from operator import attrgetter

        
def tournament(population, size=10):
    
    """Tournament selection implementation.

    Requires: population we want to select from; size of tournaments

    Ensures: selected individual
    """
    
    # Select individuals based on tournament size
    tournament = sample(population.individuals, size)
    # Check if the problem is max or min
    if population.optim == 'max':
        return max(tournament, key=attrgetter("fitness"))
    elif population.optim == "min_errors" or population.optim == "min_45sum" or population.optim == "min_factorial":
        return min(tournament, key=attrgetter("fitness"))
    else:
        raise Exception("No optimiziation specified")


def rank(population):
    """Rank selection implementation.

    Requires: population we want to select from.

    Ensures: selected individual
    """
    
    # Rank individuals based on optim approach
    if population.optim == 'max':
        population.individuals.sort(key=attrgetter('fitness'))
    elif population.optim == "min_errors" or population.optim == "min_45sum" or population.optim == "min_factorial":
        population.individuals.sort(key=attrgetter('fitness'), reverse=True)

    # Sum all ranks
    total = sum(range(population.size+1))
    # Get random position
    spin = uniform(0, total)
    position = 0
    # Iterate until spin is found
    for count, individual in enumerate(population):
        position += count + 1
        if position > spin:
            return individual
        

def roulette(population):
    """Roulette wheel selection implementation.

    Requires: population we want to select from.

    Ensures: selected individual
    """

    if population.optim == "max":
        # Sum total fitnesses
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual
            
            
    elif population.optim == "min_errors" or population.optim == "min_45sum" or population.optim == "min_factorial":
        
        # Sum total 1/fitnesses for min
        total_fitness = sum([1/i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += 1/individual.fitness
            if position > spin:
                return individual

    else:
        raise Exception("No optimiziation specified (min or max).")

           
def stochastic(population):
    
    """Stochastic Universal Sampling implementation.

    Requires: population we want to select from.

    Ensures: selected individualS (both 2, chosen at once)
    """
    
    if population.optim == "max":
        # Sum total fitnesses
        total_fitness = sum([i.fitness for i in population])
        #define interval btw pointers accoridng to pop size
        pointer_interval = total_fitness/2 #coz we want to select 2 individuals
        # Get both 'positions' on the wheel
        spin1 = uniform(0, total_fitness)
        if spin1 > pointer_interval:
            spin2 = spin1 - pointer_interval
        else:
            spin2 = spin1 + pointer_interval
        #intitiates list to store selected individuals
        individuals_stochastic = []
        position = 0
        i = 0
        
        for individual in population:
            #finds individuals
            position += individual.fitness
            if (position > spin1 or position  > spin2) and len(individuals_stochastic) == 0:
                individuals_stochastic.append(i)
            if position > spin1 and position > spin2:
                individuals_stochastic.append(i)
            if len(individuals_stochastic) == 2:
                break
            
            i+=1
        
        return individuals_stochastic
            
    elif population.optim == "min_errors" or population.optim == "min_45sum" or population.optim == "min_factorial":
         # Sum total fitnesses
        total_fitness = sum([1/i.fitness for i in population])
        #define interval btw pointers accoridng to pop size
        pointer_interval = total_fitness/2 #coz we want to select 2 individuals
        # Get both 'positions' on the wheel
        spin1 = uniform(0, total_fitness)
        if spin1 > pointer_interval:
            spin2 = spin1 - pointer_interval
        else:
            spin2 = spin1 + pointer_interval
        #intitiates list to store selected individuals
        individuals_stochastic = []
        position = 0
        i = 0
        
        for individual in population:
            #finds individuals
            position += 1/individual.fitness
            if (position > spin1 or position  > spin2) and len(individuals_stochastic) == 0:
                individuals_stochastic.append(i)
            if position > spin1 and position > spin2:
                individuals_stochastic.append(i)
            if len(individuals_stochastic) == 2:
                break
            
            i+=1
            
         
        return individuals_stochastic
    
    else:
        raise Exception("No optimiziation specified (min or max).")
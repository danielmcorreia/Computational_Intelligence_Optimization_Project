from random import randint, sample

def single_point_co(p1, p2):
    
    """Implementation of ROW-WISE single point crossover

    Requires:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    REnsures
        Individuals: Two offspring, resulting from the crossover.
    """
    
    co_row = randint(0, len(p1)-1)
    co_point = randint(0, len(p1[co_row])-1)
    
    offspring1 = p1
    offspring2 = p2
    
    offspring1[co_row] = p1[co_row][:co_point] + p2[co_row][co_point:]
    offspring2[co_row] = p2[co_row][:co_point] + p1[co_row][co_point:]
    
    return offspring1, offspring2 


def cycle_co(p1, p2):
    
    """Implementation of ROW-WISE cycle crossover.

    Requires:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    REnsures
        Individuals: Two offspring, resulting from the crossover.
    """
    
    # Offspring placeholders - None values make it easy to debug for errors
    offspring1 = []
    offspring2 = []
    for row in p1:
        offspring1.append([None] * len(row))
        offspring2.append([None] * len(row))
    
    #iterates through each row of the offspring
    for row_idx, row in enumerate(offspring1):
        
        # While there are still None values in offspring, get the first index of
        # None and start a "cycle" according to the cycle crossover method
        while None in row:

            #index of gene in present row
            index = row.index(None)

            # alternate parents between cycles beginning on second cycle
            if index != 0:
                p1, p2 = p2, p1
            val1 = p1[row_idx][index]
            val2 = p2[row_idx][index]
            
            while val1 != val2:
                offspring1[row_idx][index] = p1[row_idx][index]
                offspring2[row_idx][index] = p2[row_idx][index]
                val2 = p2[row_idx][index]
                index = p1[row_idx].index(val2)
                
            # In case last values share the same index, fill them in each offspring
            offspring1[row_idx][index] = p1[row_idx][index]
            offspring2[row_idx][index] = p2[row_idx][index]

    return offspring1, offspring2



def pmx_co(p1, p2):
    
    """Implementation of ROW-WISE PMX crossover.

    Requires:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    REnsures
        Individuals: Two offspring, resulting from the crossover.
    """
    
    offspring1 = []
    offspring2 = []
    
    def choose_co_points(len_row):
        
        # Sample 2 random co points
        co_points = sample(range(len_row), 2)
        co_points.sort()
        
        return co_points

    def PMX(x, y, len_row, idx_row):
        
        # Create placeholder for offspring
        o = [None] * len_row
    
        co_points = choose_co_points(len_row)
        
        # Copy co segment into offspring
        o[co_points[0]:co_points[1]] = x[idx_row][co_points[0]:co_points[1]]
        
        # Find set of values not in offspring from co segment in P2
        z = set(y[idx_row][co_points[0]:co_points[1]]) - set(x[idx_row][co_points[0]:co_points[1]])

        # Map values in set to corresponding position in offspring
        for i in z:
            temp = i
            index = y[idx_row].index(x[idx_row][y[idx_row].index(temp)])
            while o[index] != None:
                temp = index
                index = y[idx_row].index(x[idx_row][temp])
            o[index] = i
        
        while None in o:
            index = o.index(None)
            o[index] = y[idx_row][index]
            
        return o
    
    #iterates through all rows of parents
    for idx_row, row in enumerate(p1):

        o1, o2 = (PMX(p1, p2, len(row), idx_row), PMX(p2, p1, len(row), idx_row))
        
        offspring1.append(o1)
        offspring2.append(o2)
        

    return offspring1, offspring2

import numpy as np

def set_grids(solution):
    '''Takes a canditate solved sudoku and stores the contents of each 3x3 grid in a list. In total, it creates a list
    of 9 lists, each list corresponding to a 3x3 square whose elements, in theory, should be all unique'''
    
    squares = []

    for row in range(0,7,3):
        for column in range(0,7,3):
            current_square = solution[row:row+3,column:column+3].flatten().tolist()
            squares.append(current_square)
            
    return squares


def max_cardinality(solution):
    
    '''Fitness function for maximization problem: assesses an individual's fitness by counting the number of unique
    numbers existing in each row, column and square'''
    
    fitness = 0 #fitness = cardinality
            
    # checks cardinality in rows
    for row in solution:
        fitness += len(set(row))
                
    # checks cardinality in columns
    for column in np.array(solution).T.tolist():
        fitness += len(set(column))
        
    # checks cardinality in 3x3 grids
    for square in set_grids(solution):
        fitness += len(set(square))   
      
    return fitness


def min_errors(solution):
    '''Fitness function for minimization problem: assesses an individual's fitness by counting the number of errors
    identified in each row, column and the relevant 3x3 squares
    '''
    
    #Step 1:  Initializes variable to count number of mistakes in each row, column and grid
    errors = 0

    #Step 2: Cycle through rows and count number of times each digit appears
    for row in solution.tolist():
        # converts list(row) to dict
        dict_count = {i: row.count(i) for i in row}

        # cycles through dict and checks whether digits are repeated
        for key in dict_count:
            #if repeat occurs, add 1 to problems
            if dict_count[key] > 1:
                errors += dict_count[key] - 1

    #Step 3: Transpose solution in order to convert columns into lists and repeat process for each column
    tranposted_solution = np.array(solution).T.tolist()

    for column in tranposted_solution:
        dict_count = {i: column.count(i) for i in column}

        for key in dict_count:
            if (dict_count[key] > 1):
                errors += dict_count[key] - 1

    #Step 4: Assess number of repetitions in 3 by 3 grid

    squares = set_grids(solution)
    #repeat assessment process and compute errors in grid
    for square in squares:
        dict_count = {i: square.count(i) for i in square}
        for key in dict_count:
            if (dict_count[key] > 1):
                errors += dict_count[key] - 1
    
    return errors


def min_45sum(solution):
    ''' intended as minimization problem,
    fitness is computed as the sum of the difference in absolute value between the expected result (45) and the real value for each
    row, column and grid
    '''
    
    #Step 1:  Initializes variables to count number of mistakes in each row, column and grid
    sum_ = 0

    #Step 2: Cycle through rows (compute sum of row and store it in vector)
    for row in solution:
        # appends the sum of a row to result
        sum_ += abs(45 - np.sum(row))

    #Step 3: Transpose solution in order to convert columns into lists and repeat process for each column
    tranposted_solution = np.array(solution).T.tolist()

    for column in tranposted_solution:
        sum_ += abs(45 - np.sum(column))

    #Step 4: Assess value of sum inside each 3 by 3 grid
    squares = set_grids(solution)
    # repeat assessment process and compute errors in grid
    for square in squares:
        sum_ += abs(45 - np.sum(square))

    #Step 5: By now, we should have three (1 x 9) lists.
    #The sum of elements in each row, column or grid of a sudoku puzzle should be 45. Therefore, we will make the comparison:
    #Start by creating 1 by 9 list where each value is 45.
    
    return sum_


def min_factorial(solution, penalty = False):
    ''' intended as minimization problem,
    computes product of elements in row, column and 3x3 grid
    fitness is computed as the sum of the difference in absolute value between the expected result (9 factorial) and the real value
    '''
    
    #Step 1:  Initializes variables to count number of mistakes in each row, column and grid
    factorial = 0

    #Step 2: Cycle through rows (compute sum of row and store it in vector)
    for row in solution:
        factorial_ = 1
        for number in row:
            factorial_ = factorial_*number
        factorial += abs(362880 - factorial_)

    #Step 3: Transpose solution in order to convert columns into lists and repeat process for each column
    tranposted_solution = np.array(solution).T.tolist()
        
    for column in tranposted_solution:
        factorial_ = 1
        for number in column:
            factorial_ = factorial_*number
        factorial += abs(362880 - factorial_  )
    
    #Step 4: Assess value of sum inside each 3 by 3 grid
    squares = set_grids(solution)
    # repeat assessment process and compute errors in grid
    for square in squares:
        factorial_ = 1
        for number in square:
            factorial_ = factorial_*number
        factorial += abs(362880 - factorial_  )
    
    return factorial
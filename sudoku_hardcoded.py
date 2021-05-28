#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  9 11:59:51 2021

@author: Daniel
"""

import numpy as np
from get_sudoku import get_sudoku_
from copy import deepcopy

def look_row(row):
    
    
    #creates local set for current square
    local_set_row = {i for i in range(1,10)}

    #iterates through elements of row of current square
    for element in row:
        #eleminates number from local set if present in row
        #this will reduce the possibilities of numbers to be put on current square
        if element in local_set_row:
            local_set_row.remove(element)

    return local_set_row


def look_column(column):
    
    #creates local set for current square
    local_set_column = {i for i in range(1,10)}
    
    #iterates through elements of column of current square
    for element in column:
        
        #eliminates number from local set if present in row
        #this will reduce the possibilities of numbers to be put on current square
        if element in local_set_column:
            local_set_column.remove(element)
            
    return local_set_column



def get_square(sudoku, row, column):
    
    #finds square where current cell is located
    
    if row in range(0,3):
        if column in range(0,3):
            search_square = sudoku[0:3,0:3]
        if column in range(3,6):
            search_square = sudoku[0:3,3:6]
        if column in range(6,9):
            search_square = sudoku[0:3,6:9]
    if row in range(3,6):
        if column in range(0,3):
            search_square = sudoku[3:6,0:3]
        if column in range(3,6):
            search_square = sudoku[3:6,3:6]
        if column in range(6,9):
            search_square = sudoku[3:6,6:9]
    if row in range(6,9):
        if column in range(0,3):
            search_square = sudoku[6:9,0:3]
        if column in range(3,6):
            search_square = sudoku[6:9,3:6]
        if column in range(6,9):
            search_square = sudoku[6:9,6:9]
            
    return search_square



def look_square(sudoku, row, column):
    
    #creates local set for current square
    local_set_square = {i for i in range(1,10)}
    
    #finds square where current cell is located
    search_square = get_square(sudoku, row, column)
    
    #iterates through elements of column of current square
    for row in search_square:
        for column in row:
        
        #eleminates number from local set if present in row
        #this will reduce the possibilities of numbers to be put on current square
            if column in local_set_square:
                local_set_square.remove(column)
            
    return local_set_square



def intercept_locals(local_set_row, local_set_column, local_set_square):
    
    #intercepts sets of possible numbers to put on current square according to
    #evaluation of row, column and big square
    
    local_set = local_set_row.intersection(local_set_column)
    
    local_set = local_set.intersection(local_set_square)
    
    return local_set 



def get_candidates(sudoku):
    
    candidates = sudoku.tolist()
    
    #starts searching by row
    for i in range(0,9):
            
        #iterates through column of said row
        for j in range(0,9):
            
            #only interested in squares that don't already have a number assigned
            if sudoku[i,j] == 0:
                    
                #look row
                set_row = look_row(sudoku[i])
                    
                #look column
                set_column = look_column(sudoku[:,j])
                
                #look big square
                set_square = look_square(sudoku, i, j)
                
                #intercept all
                local_set = intercept_locals(set_row, set_column, set_square)
                
                #
                candidates[i][j] = list(local_set)
            
            else:
                candidates[i][j] = [sudoku[i,j]]
    
    return candidates


def filter_candidates(sudoku):
    test_sudoku = sudoku.copy()
    candidates = get_candidates(sudoku)
    filtered_candidates = deepcopy(candidates)
    for i in range(9):
        for j in range(9):
            # Check for empty cells
            if sudoku[i][j] == 0:
                for candidate in candidates[i][j]:
                    # Use test candidate
                    test_sudoku[i][j] = candidate
                    # Remove candidate if it produces an invalid grid
                    if not check_solution(fill_singles(test_sudoku)):
                        filtered_candidates[i][j].remove(candidate)
                        
                    # Revert changes
                    test_sudoku[i][j] = 0
                    
    return filtered_candidates



def fill_singles(sudoku, candidates=None):
    
    sudoku = sudoku.copy()
    
    if not candidates:
        candidates = get_candidates(sudoku)
    
    singles = True
    
    while singles:
        
        singles = False
        
        for i in range(0,9):
            for j in range(0,9):
                if type(candidates[i][j]) == list:
                    
                    if len(candidates[i][j]) == 1 and sudoku[i, j] == 0:
                        sudoku[i, j] = candidates[i][j][0]
                        
                        candidates = merge(get_candidates(sudoku), candidates)
                        
                        singles = True
                             
    return sudoku



def merge(candidates_1, candidates_2):

    candidates_min = []
    for i in range(9):
        row = []
        for j in range(9):
            if len(candidates_1[i][j]) < len(candidates_2[i][j]):
                row.append(candidates_1[i][j][:])
            else:
                row.append(candidates_2[i][j][:])

        candidates_min.append(row)
        
    return candidates_min
    
   
def make_guess(sudoku, candidates=None):
    
    print("Making guesses, still on it :(")
    
    min_len = 9
    
    sudoku = sudoku.copy()
    if not candidates:
        candidates = get_candidates(sudoku)

    
    for i in range(9):
        for j in range(9):
            
            #checks if current cell in memory is set to unique value or is still undecided
            if type(candidates[i][j]) == list:
                
                #finds list with lowest lentgh to maximize hypothesis of getting substitution right
                if len(candidates[i][j]) < min_len:
                    min_len = len(candidates[i][j])
                    
    for i in range(9):
        for j in range(9):
            
            if type(candidates[i][j]) == list:
                if len(candidates[i][j]) == min_len:
                    for guess in candidates[i][j]:
                        sudoku[i][j] = guess
                        solution = filtered_solve(sudoku)
                        if solution is not None:
                            return solution
                        # Discarding incorrect guess
                        sudoku[i][j] = 0
                        

def check_solution(sudoku):
    
    '''checks whether solution is valid (particularly useful after making guess)'''
    
    candidates = get_candidates(sudoku)
    
    for i in range(0, 9):
        for j in range(0, 9):
            
            #checks if in candidates list there are lists with no values (=cells with no candidates)
            if type(candidates[i][j]) == list:
                if len(candidates[i][j]) == 0:
                    return False
                
    return True


def is_solution(sudoku):

    if np.all(np.sum(sudoku, axis=1) == 45) and \
       np.all(np.sum(sudoku, axis=0) == 45):
           
           if sum(map(sum, sudoku[0:3, 0:3])) == 45 and sum(map(sum, sudoku[0:3, 3:6])) == 45 and sum(map(sum, sudoku[0:3, 6:9])) == 45 and \
               sum(map(sum, sudoku[3:6, 0:3])) == 45 and sum(map(sum, sudoku[3:6, 3:6])) == 45 and sum(map(sum, sudoku[3:6, 6:9])) == 45 and \
                   sum(map(sum, sudoku[6:9, 0:3])) == 45 and sum(map(sum, sudoku[6:9, 3:6])) == 45 and sum(map(sum, sudoku[6:9, 6:9])) == 45:
                       return True
    return False               


def filtered_solve(sudoku):
    
    candidates = filter_candidates(sudoku)
    sudoku = fill_singles(sudoku, candidates)
    if is_solution(sudoku):
        return sudoku
    if not check_solution(sudoku):
        return None
    return make_guess(sudoku, candidates)
  
               
def solve(sudoku):
    
    sudoku = fill_singles(sudoku)

    if is_solution(sudoku):
        print(sudoku)
        return sudoku
    if not check_solution(sudoku):
        return None

    return make_guess(sudoku)


solve(get_sudoku_())

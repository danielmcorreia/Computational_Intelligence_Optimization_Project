#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 23:21:33 2021

@author: Daniel
"""

import numpy as np

#EASY
easy = np.array([[8, 1, 0, 0, 3, 0, 0, 2, 7], 
                 [0, 6, 2, 0, 5, 0, 0, 9, 0], 
                 [0, 7, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 9, 0, 6, 0, 0, 1, 0, 0], 
                 [1, 0, 0, 0, 2, 0, 0, 0, 4], 
                 [0, 0, 8, 0, 0, 5, 0, 7, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 8, 0], 
                 [0, 2, 0, 0, 1, 0, 7, 5, 0], 
                 [3, 8, 0, 0, 7, 0, 0, 4, 2]])

#MEDIUM
medium = np.array([[0, 0, 0, 0, 6, 0, 5, 0, 0],
                   [2, 0, 0, 0, 0, 3, 0, 0, 0],
                   [0, 0, 3, 9, 0, 4, 8, 0, 0],
                   [0, 4, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 2, 0, 0, 0, 0],
                   [0, 3, 2, 7, 1, 5, 4, 0, 6],
                   [0, 7, 8, 5, 4, 1, 9, 0, 0],
                   [4, 0, 0, 0, 7, 0, 0, 8, 0],
                   [0, 6, 1, 0, 9, 0, 3, 0, 0]])

#HARD
hard = np.array([[1, 0, 0, 5, 0, 0, 0, 0, 7],
                 [0, 0, 0, 0, 4, 6, 0, 0, 0],
                 [2, 0, 0, 0, 7, 0, 6, 0, 0],
                 [0, 0, 8, 2, 0, 0, 0, 0, 9],
                 [0, 0, 4, 0, 0, 0, 0, 0, 6],
                 [0, 0, 3, 4, 0, 8, 5, 0, 0],
                 [0, 0, 2, 7, 0, 0, 0, 3, 0],
                 [9, 0, 0, 8, 0, 0, 0, 0, 5],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0]])

def get_sudoku_():
    
    """ returns array containing the sudoku of asked difficulty
    """
    
    difficulty = input('Choose difficulty of sudoku to be solved (easy, medium, hard, expert): ')

    if difficulty == 'easy':
        sudoku = easy
    if difficulty == 'medium':
        sudoku = medium
    if difficulty == 'hard':
        sudoku = hard
    
    return sudoku
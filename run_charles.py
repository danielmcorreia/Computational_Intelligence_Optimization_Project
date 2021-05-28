#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 14 16:06:59 2021

@author: Daniel
"""

from charles_sudoku import Population, Individual
from selection import *
from mutation import *
from crossover import *
import os
import numpy as np
from get_sudoku import get_sudoku_

#write name of configuration you want to use, for analysis purposes
#USE FOLLOWING FORMAT FOR ORGANIZATION PURPOSES: difficulty_popsize_optim_replacement_gens_select_cross_mutate_cop_mup_elitism
name_configuration = input('Write description of desired configuration: ')

#asks user for difficulty input and gets data
sudoku = get_sudoku_()

#create folder for this specific configuration
os.makedirs('Runs/' + name_configuration)

#create for loop to run charles as many time as tou want for stat analysis
for i in range(100):

    pop = Population(
        size=2000, optim="max", sudoku=sudoku, run=i)

    pop.evolve(
        gens=40,
        select=tournament,
        crossover= cycle_co,
        mutate=swap_mutation,
        co_p=0.8,
        mu_p=0.8,
        elitism=True,
        sudoku=sudoku,
        run=i)
    
    print('------------------------------------------------------')
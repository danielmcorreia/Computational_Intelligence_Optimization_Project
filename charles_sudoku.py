#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 8 04:18:42 2021

@author: Daniel
"""

from random import shuffle, choice, sample, random, randint, uniform
from operator import attrgetter
from copy import deepcopy
import numpy as np
from selection import *
from mutation import *
from crossover import *
from fitness_functions import *
from random import random
from operator import  attrgetter
import csv, time, glob, os


class Individual:
    
    def __init__(self, optim=None, representation=None,size=None,sudoku=None,):
        
        '''initiates sudoku with hard coded constrain:
            initialize the sudoku grid by row, allowing only one number through 1 to 9 to be placed in each row'''
            
        if representation == None:
            
            representation_rows = []
            for row in sudoku:
                valid_set_row = [i for i in range(1,10)]
                take_out_set = row[row!=0].tolist()  
                for number in take_out_set:
                    valid_set_row.remove(number)
                row = sample(valid_set_row, len(valid_set_row))
                representation_rows.append(row)

            self.representation = representation_rows
            
            
        else:
            self.representation = representation
            
        self.fitness = self.evaluate(optim, sudoku)
        
        
    def evaluate(self, optim, sudoku):
        
        #creates copy of current sudoku being solved AND of current individual whose fitness is under evaluation
        solution = deepcopy(sudoku)
        copy_individual = deepcopy(self.representation)    
        
        #Let's fill in the sudoku matrix with the current individual, where == 0 (original # are mantained)
        for idx,row in enumerate(solution):

            for idy, col in enumerate(row):
                if col == 0:
                    #replaces space in solution by corresponding gene of current individual
                    solution[idx][idy] = copy_individual[idx][0]
                    copy_individual[idx].pop(0)        
        

        #Evaluates fitness of current individual here; returns fitness of individual
        
        if optim == 'min_errors':
            return min_errors(solution)
        
        if optim == 'max':
            return max_cardinality(solution)
        
        if optim == 'min_45sum':
            return min_45sum(solution)
        
        if optim == 'min_factorial':
            return min_factorial(solution)
            

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness}"


class Population:
    
    def __init__(self, size, optim, sudoku, run, **kwargs):
        
        print('Run: ' + str(run + 1))
        
        self.individuals = []
        self.size = size
        self.optim = optim
        self.gen = 1
        self.timestamp = int(time.time())
        for _ in range(size):
            self.individuals.append(
                Individual(
                    optim=optim,
                    sudoku=sudoku,
                )
            )
            
    def evolve(self, gens, select, crossover, mutate, co_p, mu_p, elitism, sudoku, run):
        
        for gen in range(gens):
            new_pop = []
            if elitism == True:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min_errors" or self.optim == "min_45sum" or self.optim == "min_factorial":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))
            
            while len(new_pop) < self.size:
                
                if select == stochastic: #this wheel should be turned only once to avoid bias like in roulette wheel

                    list_idx_individuals = select(self)
                    parent1, parent2 = self[list_idx_individuals[0]], self[list_idx_individuals[1]]
                    
                if select != stochastic:
                    parent1, parent2 = select(self), select(self)
                
                    
                # Crossover
                if random() < co_p:
                    
                    offspring1, offspring2 = crossover(parent1, parent2)
                    
                else:
                    offspring1, offspring2 = parent1, parent2
                
                # Mutation
                if random() < mu_p:

                    offspring1 = mutate(offspring1)

                if random() < mu_p:
                    offspring2 = mutate(offspring2)
                
                
                new_pop.append(Individual(representation=offspring1, optim=self.optim, sudoku=sudoku))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2, optim=self.optim, sudoku=sudoku))
            
            
            if elitism == True:
                if self.optim == "max":
                    least = min(new_pop, key=attrgetter("fitness"))
                elif self.optim == "min_errors" or self.optim == "min_45sum" or self.optim == "min_factorial":
                    least = max(new_pop, key=attrgetter("fitness"))
                new_pop.pop(new_pop.index(least))
                new_pop.append(elite)
            
            
            self.individuals = new_pop
            
            
            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
                                      
            elif self.optim == "min_errors" or self.optim == "min_45sum" or self.optim == "min_factorial":
                print(f'Best Individual: {min(self, key=attrgetter("fitness"))}')
                
            
            self.log(run, gens)
            self.gen += 1
    
    
    def log(self, run, gens):
        
        #logs necessary data for further analysis
        
         with open(max(glob.glob('Runs/*'), key=os.path.getctime) + '/' + f'run_{run}.csv', 'a', newline = '') as file:
                writer = csv.writer(file)
                for i in self:
                    writer.writerow([self.gen, i.fitness, i.representation])
            
    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]

    def __repr__(self):
        return f"Population(size={len(self.individuals)}, individual_size={len(self.individuals[0])})"
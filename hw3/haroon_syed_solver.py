#!/usr/bin/python

import numpy as np
import sys
from sets import Set
from collections import deque

'''
File reading function for sudoku
Input: filename
Output: a list of 2D numpy matrices representing sudokus
'''
def read_sudoku(fname):
    with open(fname) as f:
        f_input = [x.strip('\r\n') for x in f.readlines()]

    sudoku_list = []
    for i in xrange(len(f_input)):
        sudoku = np.zeros((9, 9))
        temp = f_input[i]
        for j in xrange(0, len(temp), 9):
            sudoku_row = temp[j:j + 9]
            for k in xrange(0, 9):
                sudoku[j / 9][k] = sudoku_row[k]
        sudoku_list.append(sudoku)

    return sudoku_list


'''
Printing function for sudoku,
Input: a 2D numpy matrix
'''
def print_sudoku(sudoku):
    print '+-------+-------+-------+'
    for i in xrange(0, 9):
        for j in xrange(0, 9):
            if j == 0:
                print '|',
            if sudoku[i][j] != 0:
                print int(sudoku[i][j]),
            else:
                print '*',
            if (j + 1) % 3 == 0:
                print '|',
        print ''
        if (i + 1) % 3 == 0:
            print '+-------+-------+-------+'
    print ''


'''
Utility function for finding constraints
Input: coordinate [row, col]
Output: constraints
'''
def get_constraint(coordinate, sudoku):
    value = sudoku[coordinate[0]][coordinate[1]]
    if value == 0:
        row = sudoku[coordinate[0], :]
        col = sudoku[:, coordinate[1]]

        row_constraint = row[np.nonzero(row)]
        col_constraint = col[np.nonzero(col)]
        block = get_block(coordinate, sudoku)

        blo_constraint = block[np.nonzero(block)]

        all_constraint = np.unique(np.concatenate((row_constraint, col_constraint, blo_constraint)))
        return all_constraint
    else:
        print 'not a variable'


'''
Utility function for getting a 3x3 sudoku block given a coordinate
Input: coordinate [row, col]
Output: 3x3 numpy matrix
'''
def get_block(coordinate, sudoku):
    row_range = [3 * (coordinate[1] / 3), 3 * (coordinate[1] / 3) + 3]
    col_range = [3 * (coordinate[0] / 3), 3 * (coordinate[0] / 3) + 3]

    return sudoku[col_range[0]:col_range[1], row_range[0]:row_range[1]]




def print_Set(sat):
    A = ['A','B','C','D','E','F','G','H','I']
    B = [1,2,3,4,5,6,7,8,9]
    for a in range(0,9):
        for b in range(0,9):
            if sat[a][b] != 0:
                print A[a],B[b], sat[a][b]

'''
intializes domain
'''
def get_domain(sudoku):
    X = np.copy(sudoku)
    D = [[0 for x in range(9)] for y in range(9)] #Domain
    cue = deque()
    for a in range(0,9):
        for b in range(0,9):
            if X[a][b] == 0:
                D[a][b] = []
                cue.append([a,b])
                const = get_constraint([a,b],sudoku)
                for i in range(1,10):
                    if i not in const:
                        D[a][b].append(i)

    return X,D,cue

def revise_domain(value,p1,p2,sudoku):
    X = np.copy(sudoku)
    X[p1][p2] = value
    cue = deque()
    D = [[0 for x in range(9)] for y in range(9)] #Domain
    for a in range(0,9):
        for b in range(0,9):
            if X[a][b] == 0:
                cue.append([a,b])
                const = get_constraint([a,b],X)
                D[a][b] = []
                for i in range(1,10):
                    if i not in const:
                        D[a][b].append(i)
    return X,D,cue

def check_if_goal(sudoku):
    for a in range(0,9):
        for b in range(0,9):
            if sudoku[a][b] == 0:
                return False
    return True


def min_value(D):
    mini = 10
    pos = 0
    for a in range (0,9):
        for b in range(0,9):
            if D[a][b] != 0:
                cur_min = len(D[a][b])
                if(cur_min < mini):
                    mini = cur_min
                    pos = [a,b]
    return pos

'''
AC-3 Algorithm
Input: 2D numpy matrix
Output: return True if a solution is found, with solved sudoku, False otherwise, with original sudoku
'''
def ac3(sudoku):
    # TODO
    #solved_sudoku = np.copy(sudoku)
    X,D,cue = get_domain(sudoku) 
    #print_Set(D)   
    while(len(cue) != 0):
        pos = cue.pop()
        px = pos[0]
        py = pos[1]
        dsize = len(D[px][py])
        if(dsize == 1):
            t = D[px][py]
            val = t[0]
            X,D,cue = revise_domain(val,px,py,X)
            if(check_if_goal(X)):
                return True,X

    return False, X


#global globe
#globe = 0

def b_helper(X, D, cue):
    goal = False
    if (
        check_if_goal(X)):
        global globe
        globe = np.copy(X)
        goal = True
        return True, X
    pos = min_value(D)
    px = pos[0]
    py = pos[1]
    vals = D[px][py]
    size = len(vals)
   # print 'pos',pos
    #print vals
    for i in range(0,size):
        v = vals[i]
        X,D,cue = revise_domain(v,px,py,X)
        if((b_helper(X,D,cue))[0] == True):
           # print 'backtrack'
            return True,X
        X[px][py] = 0
    return False, X





'''
Backtracking search Algorithm
Input: 2D numpy matrix
Output: return True if a solution is found, with solved sudoku, False otherwise, with original sudoku
'''
def bts(sudoku):
    # TODO
    solved_sudoku = np.copy(sudoku)
    X,D,cue = get_domain(sudoku)
    solved,X = b_helper(X,D,cue)
    #print solved
    #print globe
    X = np.copy(globe)
    return solved, X
    #return False, solved_sudoku

'''
Main function
'''
def main():
    sudoku_list = read_sudoku(sys.argv[1])
    solved_sudokus = []
    for sudoku in sudoku_list:
        print_sudoku(sudoku)
        if sys.argv[2] == 'ac3':
            print 'Using AC-3'
            solved, ret_sudoku = ac3(sudoku)
            if solved:
                print 'Solved Sudoku'
                print_sudoku(ret_sudoku)
            else:
                print 'No solution found'
            solved_sudokus.append(ret_sudoku.flatten())
        elif sys.argv[2] == 'bts':
            print 'Using backtracking search'
            solved, ret_sudoku = bts(sudoku)
            if solved:
                print 'Solved Sudoku'
                print_sudoku(ret_sudoku)
            else:
                print 'No solution found'
            solved_sudokus.append(ret_sudoku.flatten())
        else:
            print 'No such type'
        print ''
    np.savetxt('sudoku_solutions_'+sys.argv[2]+'.txt', solved_sudokus, fmt='%d', delimiter='')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Arguments error'
    else:
        main()

import sys
from CellularAutomata import CellularAutomata
from Grid2D import Grid2D_Fixed, Grid2D_Periodic, Grid2D_Reflective
from GUI import GUILoop
from numpy import random

class GameOfLife(CellularAutomata):
    pass
    ALIVE = 1
    DEAD  = 0
    PROBABILITY = 0.25

    def __init__(self):
        self.m_TimeStep = 0

    def initCond(self):
        for j in range(0, self.m_Grid2D.getHeight()):
            for i in range(0, self.m_Grid2D.getWidth()):
                state = GameOfLife.DEAD
                if random.random() < GameOfLife.PROBABILITY:
                    state = GameOfLife.ALIVE
                self.m_Grid2D.initCond(j, i, state)


    def update(self):
        '''
        Orientação da vizinhança
                nw | n | ne
               ----|---|----
                w  | c |  e
               ----|---|----
                sw | s | se
        '''
        nw = -1
        n  = -1
        ne = -1
        w  = -1
        e  = -1
        sw = -1
        s  = -1
        se = -1
        c  = -1
        sum = 0
        for j in range(0, self.m_Grid2D.getHeight()):
            for i in range(0, self.m_Grid2D.getWidth()):
                nw = self.m_Grid2D.getState(j+1, i-1)
                n  = self.m_Grid2D.getState(j+1, i)
                ne = self.m_Grid2D.getState(j+1, i+1)
                w  = self.m_Grid2D.getState(j, i-1)
                c  = self.m_Grid2D.getState(j, i)
                e  = self.m_Grid2D.getState(j, i+1)
                sw = self.m_Grid2D.getState(j-1, i-1)
                s  = self.m_Grid2D.getState(j-1, i)
                se = self.m_Grid2D.getState(j-1, i+1)
                sum = nw + n + ne + w + e + sw + s + se
                if sum == 3 and c == 0:
                    self.m_Grid2D.setState(j, i, GameOfLife.ALIVE)
                elif sum >= 2 and sum <= 3 and c == 1:
                    self.m_Grid2D.setState(j, i, GameOfLife.ALIVE)
                else:
                    self.m_Grid2D.setState(j, i, GameOfLife.DEAD)

        CellularAutomata.update(self)



    def finalCond(self):
        print('Final')

    def name(self):
        return 'Game of Life'

if __name__ == '__main__':
    #grid = Grid2D_Fixed(128, 64)
    #grid.setConstant(0) #fixed value on the boundary condition
    #boundary = 'fixed'
    #boundary = 'periodic'
    boundary = 'reflective'
    w = 128
    h = 64

    if  boundary == 'fixed':
        grid = Grid2D_Fixed(w, h)
    elif boundary == 'periodic':
        grid = Grid2D_Periodic(w, h)
    elif boundary == 'reflective':
        grid = Grid2D_Reflective(w,h)
    else:
        print('NO BOUNDARIES CONDITION DEFINED')
        sys.exit(-1)

    CA = GameOfLife()
    CA.setGrid(grid)
    CA.initCond()
    gui = GUILoop(CA)
    #gui.setCellularAutomata(CA)
    gui.init()
    gui.loop()



    '''
    for i in range(0, 10):
        print('Step: ', i)
        CA.update()
    CA.finalCond()
    '''


    print('Hello')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

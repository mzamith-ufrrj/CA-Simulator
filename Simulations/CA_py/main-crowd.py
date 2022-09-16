import sys
from CellularAutomata import CellularAutomata
from Grid2D import Grid2D_Fixed, Grid2D_Periodic, Grid2D_Reflective
from GUI import GUILoop
from numpy import random

class Crowd(CellularAutomata):
    pass
    PERSON = 1
    FREE   = 0
    DOOR   = 2
    

    def __init__(self):
        self.m_TimeStep = 0
        self.m_W = 0
        self.m_H = 0

    def initCond(self):
        H = int(self.m_Grid2D.getHeight() / 2)
        W = int(self.m_Grid2D.getWidth() / 2)

    
        self.m_Grid2D.initCond(H, W, Crowd.DOOR)

        self.m_Grid2D.initCond(H-2, W-2, Crowd.PERSON)
        self.m_Grid2D.initCond(H-2, W, Crowd.PERSON)
        self.m_Grid2D.initCond(H-2, W+2, Crowd.PERSON)

        self.m_Grid2D.initCond(H+2, W-2, Crowd.PERSON)
        self.m_Grid2D.initCond(H+2, W, Crowd.PERSON)
        self.m_Grid2D.initCond(H+2, W+2, Crowd.PERSON)
        
        self.m_Grid2D.initCond(H, W-2, Crowd.PERSON)
        self.m_Grid2D.initCond(H, W+2, Crowd.PERSON)
        
        self.m_W = W 
        self.m_H = H

    def update(self):
        '''
        Orientação da vizinhança
                nw | n | ne
               ----|---|----
                w  | c |  e
               ----|---|----
                sw | s | se
        '''
        for j in range(0, self.m_Grid2D.getHeight()):
            for i in range(0, self.m_Grid2D.getWidth()):
                c  = self.m_Grid2D.getState(j, i)
                if c == Crowd.PERSON:
                    ni = i - self.m_W
                    nj = j - self.m_H
                    
                    #Achar o caminhp
        
    #CellularAutomata.update(self)


    def finalCond(self):
        print('Final')

    def name(self):
        return 'Game of Life'

if __name__ == '__main__':
    #grid = Grid2D_Fixed(128, 64)
    #grid.setConstant(0) #fixed value on the boundary condition
    boundary = 'fixed'
    #boundary = 'periodic'
    #boundary = 'reflective'
    w = 32
    h = 16

    if  boundary == 'fixed':
        grid = Grid2D_Fixed(w, h)
        grid.setConstant(1)
    elif boundary == 'periodic':
        grid = Grid2D_Periodic(w, h)
    elif boundary == 'reflective':
        grid = Grid2D_Reflective(w,h)
    else:
        print('NO BOUNDARIES CONDITION DEFINED')
        sys.exit(-1)

    CA = Crowd()
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

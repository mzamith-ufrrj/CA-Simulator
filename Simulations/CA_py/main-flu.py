import sys
from CellularAutomata import CellularAutomata
from Grid2D import Grid2D_Fixed, Grid2D_Periodic, Grid2D_Reflective
from GUI import GUILoop
from Color import Color
from numpy import random
import numpy as np
import matplotlib.pyplot as plt

class Flu(CellularAutomata):
    pass
    #number of states is 5
    EMPTY       = 0
    SUSCEPTIBLE = 1
    INFECTED    = 2
    RECOVERED   = 3
    DIED        = 4

    #input parameters

    DAYS        = 28
    P_INFECTED  = 0.125
    P_RECOVERED = 0.00001
    P_DIED      = 0.03

    def __init__(self):
        self.m_TimeStep = 0
        self.m_I = None
        self.m_Sus = []
        self.m_Inf = []
        self.m_Rec = []
        self.m_Died = []
        self.m_Days = []
        self.m_ElapsedDays = 0

    def initCond(self):
        self.m_I = np.zeros((self.m_Grid2D.getHeight(), self.m_Grid2D.getWidth()), dtype=np.int32)
        for j in range(0, self.m_Grid2D.getHeight()):
            for i in range(0, self.m_Grid2D.getWidth()):
                self.m_I[j][i] = 0
                self.m_Grid2D.initCond(j, i, self.SUSCEPTIBLE)
                if i == int(self.m_Grid2D.getWidth() / 2) and j == int(self.m_Grid2D.getHeight() / 2) :
                    self.m_Grid2D.initCond(j, i, self.INFECTED)
                    self.m_I[j][i] = self.DAYS


    def statistic(self):
        acc_s = 0
        acc_i = 0
        acc_r = 0
        acc_d = 0
        for j in range(0, self.m_Grid2D.getHeight()):
            for i in range(0, self.m_Grid2D.getWidth()):
                s = self.m_Grid2D.getState(j,i)
                if s == self.SUSCEPTIBLE:
                    acc_s = acc_s + 1
                elif s == self.INFECTED:
                    acc_i = acc_i + 1
                elif s == self.DIED:
                    acc_d = acc_d + 1
                elif s == self.RECOVERED:
                    acc_r = acc_r + 1

        self.m_Sus.append(acc_s)
        self.m_Inf.append(acc_i)
        self.m_Rec.append(acc_r)
        self.m_Died.append(acc_d)
        self.m_Days.append(self.m_ElapsedDays)

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
                sum = 0
                if self.m_Grid2D.getState(j+1, i-1) == self.INFECTED:
                    sum = sum + 1
                if self.m_Grid2D.getState(j+1, i)  == self.INFECTED:
                    sum = sum + 1
                if self.m_Grid2D.getState(j+1, i+1) == self.INFECTED:
                    sum = sum + 1
                if self.m_Grid2D.getState(j, i-1) == self.INFECTED:
                    sum = sum + 1
                if self.m_Grid2D.getState(j, i+1) == self.INFECTED:
                    sum = sum + 1
                if self.m_Grid2D.getState(j-1, i-1) == self.INFECTED:
                    sum = sum + 1
                if self.m_Grid2D.getState(j-1, i) == self.INFECTED:
                    sum = sum + 1
                if self.m_Grid2D.getState(j-1, i+1) == self.INFECTED:
                    sum = sum + 1

                my_state = self.m_Grid2D.getState(j, i)
                if my_state == self.SUSCEPTIBLE:
                    if random.random() < (sum * self.P_INFECTED):
                        self.m_I[j][i] = self.DAYS
                        self.m_Grid2D.setState(j, i, self.INFECTED)
                    else:
                        self.m_Grid2D.setState(j, i, my_state)

                elif my_state == self.INFECTED:
                    self.m_I[j][i] = self.m_I[j][i] - 1
                    if self.m_I[j][i] == 0:
                        if random.random() < self.P_DIED:
                            self.m_Grid2D.setState(j, i, self.DIED)
                        else:
                            self.m_Grid2D.setState(j, i, self.RECOVERED)

                    elif random.random() < self.P_RECOVERED:
                        self.m_I[j][i] == 0
                        self.m_Grid2D.setState(j, i, self.RECOVERED)
                    else:
                        self.m_Grid2D.setState(j, i, my_state)
                else:
                    self.m_Grid2D.setState(j, i, my_state)

        self.m_ElapsedDays = self.m_ElapsedDays + 1
        CellularAutomata.update(self)
        self.statistic()


    def finalCond(self):
        print('Final')
        x = self.m_Grid2D.getWidth() * self.m_Grid2D.getHeight()
        for i in range(0, len(self.m_Sus)):
            self.m_Sus[i] = self.m_Sus[i] / x
        for i in range(0, len(self.m_Inf)):
            self.m_Inf[i] = self.m_Inf[i] / x
        for i in range(0, len(self.m_Rec)):
            self.m_Rec[i] = self.m_Rec[i] / x
        for i in range(0, len(self.m_Died)):
            self.m_Died[i] = self.m_Died[i] / x


        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.m_Days, self.m_Sus, color='black', linewidth=3)
        ax.plot(self.m_Days, self.m_Inf, color='blue', linewidth=3)
        ax.plot(self.m_Days, self.m_Rec, color='green', linewidth=3)
        ax.plot(self.m_Days, self.m_Died, color='red', linewidth=3)
        ax.legend(['Suscetível', 'Infectado', 'Recuperado', 'Morto'])
        plt.show()

    def name(self):
        return 'Flu demo based on Cellular Automaton'

if __name__ == '__main__':
    #grid = Grid2D_Fixed(128, 64)
    #grid.setConstant(0) #fixed value on the boundary condition
    #boundary = 'fixed'
    #boundary = 'periodic'
    boundary = 'fixed'
    w = 100
    h = 100
    palettes = []
    palettes.append(Color(0, 0, 0))              #black
    palettes.append(Color(255, 255, 255))        #white
    palettes.append(Color(138, 43, 226))         #BlueViolet
    palettes.append(Color(0, 191, 255))        #DeepSkyBlue
    palettes.append(Color(32, 32, 32))



    if  boundary == 'fixed':
        grid = Grid2D_Fixed(w, h)
    elif boundary == 'periodic':
        grid = Grid2D_Periodic(w, h)
    elif boundary == 'reflective':
        grid = Grid2D_Reflective(w,h)
    else:
        print('NO BOUNDARIES CONDITION DEFINED')
        sys.exit(-1)

    CA = Flu()
    CA.setGrid(grid)
    CA.initCond()
    gui = GUILoop(CA)
    gui.setPalette(palettes)
    gui.setCellularAutomata(CA)
    gui.init()
    gui.loop()
    #for i in range(0, 150):
    #    print('Dias: ', i)
    #    CA.update()
    CA.finalCond()


    '''
    for i in range(0, 10):
        print('Step: ', i)
        CA.update()
    CA.finalCond()
    '''


    print('Hello')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

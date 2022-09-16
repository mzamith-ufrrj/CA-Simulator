import numpy as np
class Grid2D_Fixed:
    def __init__(self, w, h):
        self.m_Width = w
        self.m_Height = h
        self.m_buff0 =  np.zeros((self.m_Height, self.m_Width), dtype=np.int32) #np.matrix((self.m_Height, self.m_Width), dtype=np.int8)
        self.m_buff1 =  np.zeros((self.m_Height, self.m_Width), dtype=np.int32)
        self.m_const = 0

    #In initial condition, both buffers should be set with the same state
    #in order to guarantee the correct state  render
    def initCond(self, l, c, s):
        self.m_buff1[l][c] = s
        self.m_buff0[l][c] = s


    def setConstant(self, c):
        self.m_const = c

    def setState(self, l, c, s):
        self.m_buff1[l][c] = s


    def getState(self, l, c):
        if l >= 0 and l < self.m_Height and c >= 0 and c < self.m_Width:
            return self.m_buff0[l][c]
        else:
            return self.m_const

    def getWidth (self):
        return self.m_Width

    def getHeight (self):
        return self.m_Height

    def swap(self):
        aux = self.m_buff1
        self.m_buff1 = self.m_buff0
        self.m_buff0 = aux


class Grid2D_Periodic(Grid2D_Fixed):
    pass
    def getState(self, l, c):
        l1 = l
        c1 = c

        if l1 < 0:
            l1 = self.m_Height + l1

        if l1 >= self.m_Height:
            l1 = l1 % self.m_Height


        if c1 < 0:
            c1 = self.m_Width + c1

        if c1 >= self.m_Width:
            c1 = c1 % self.m_Width

        return self.m_buff0[l1][c1]

class Grid2D_Reflective(Grid2D_Fixed):
    pass
    def getState(self, l, c):
        l1 = l
        c1 = c

        if l1 < 0:
            l1 = (l1 * -1)

        if l1 >= self.m_Height:
            l1 = self.m_Height - (l1 % self.m_Height) - 1

        if c1 < 0:
            c1 = (c1 * -1)

        if c1 == self.m_Width:
            c1 = self.m_Width - (c1 % self.m_Width) - 1

        return self.m_buff0[l1][c1]

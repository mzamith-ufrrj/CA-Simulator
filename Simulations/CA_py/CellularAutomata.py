

class CellularAutomata:
    def __init__(self, w, h):
        raise NotImplementedError()


    def initCond(self):
        raise NotImplementedError()

    def setGrid(self, g):
        self.m_Grid2D = g

    def update(self):
        self.m_TimeStep = self.m_TimeStep + 1
        self.m_Grid2D.swap()

    def getWidth (self):
        return self.m_Grid2D.m_Width

    def getHeight (self):
        return self.m_Grid2D.m_Height

    def finalCond(self):
        raise NotImplementedError()

    def name(self):
        return 'Cellular Automata'

    def getState(self, l, c):
        return self.m_Grid2D.getState(l, c)

    def getTimeStep(self):
        return self.m_TimeStep
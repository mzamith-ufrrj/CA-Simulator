import pygame
from Color import Color
from CellularAutomata import CellularAutomata
class GUILoop:
    def __init__(self, ca):
        self.m_CA = ca
        self.m_Width = 1024
        self.m_Height = 768
        self.m_FPS = 60
        self.m_Display = None
        self.m_Clock = None
        self.m_DX = 0.0
        self.m_DY = 0.0
        self.m_Running = True
        self.m_StepbyStep = True
        self.m_ShowLattice = True
        #We should define the color palette. In this example, I wrote some color in according to site: https://erikasarti.com/html/tabela-cores/
        #Remember to define one unique color for each CA state
        self.m_Palettes = []

        self.m_Palettes.append(Color(0, 255, 0))                        #Green    # It's green, the same color of lattice color <----
        self.m_Palettes.append(Color(255, 0, 0))                        #Red
        self.m_Palettes.append(Color(0, 250, 154))                      #MediumSpringGreen
        self.m_Palettes.append(Color(0, 0, 255))                        #Blue

        self.m_Palettes.append(Color(255, 0, 255))                      #Fuchsia / Magenta
        self.m_Palettes.append(Color(255, 255, 0))                      #Yellow
        self.m_Palettes.append(Color(0, 255, 255))                      #Aqua / Cyan

        self.m_Palettes.append(Color(70, 130, 180))                     #SteelBlue
        self.m_Palettes.append(Color(221, 160, 221))                    #Plum
        self.m_Palettes.append(Color(173, 255, 47))                     #GreenYellow

        self.m_Palettes.append(Color(85, 107, 47))                      #DarkOliveGreen
        self.m_Palettes.append(Color(255, 228, 196))                    #Bisque
        self.m_Palettes.append(Color(106, 90, 205))                     #SlateBlue
        print('--------------------------------------------')
        print('Color palette size:', len(self.m_Palettes))
        print('--------------------------------------------')
        self.help()

    def setPalette(self, p):
        self.m_Palettes = []
        self.m_Palettes = p
        print('--------------------------------------------')
        print('Color palette size:', len(self.m_Palettes))
        print('--------------------------------------------')

    def setCellularAutomata(self, ca):
        self.m_CA = ca

    #m_CA does not have to be empty or none.
    def init(self):
        pygame.init()
        self.m_Display = pygame.display.set_mode((self.m_Width, self.m_Height))
        pygame.display.set_caption(self.m_CA.name())
        self.m_Display.fill((0, 0, 0))
        self.m_Clock = pygame.time.Clock()
        self.m_DX = (self.m_Width / self.m_CA.getWidth())
        self.m_DY = (self.m_Height / self.m_CA.getHeight())

    #main loop
    def loop(self):
        while self.m_Running:
            self.input()
            if not self.m_StepbyStep:
                self.update()
            self.render()

    #input key - only for render
    def input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:                                   #close window
                self.m_Running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:                               #close window
                    self.m_Running = False
                if e.key == pygame.K_e:                                 #enable step by step
                    self.m_StepbyStep = not self.m_StepbyStep
                if e.key == pygame.K_l:                                 #show lattice
                    self.m_ShowLattice = not self.m_ShowLattice
                if e.key == pygame.K_u:                                 #update steps
                    self.m_CA.update()
                if e.key == pygame.K_s:                                 #save to file - the time step is part of name
                    self.toPNG()
                if e.key == pygame.K_h:
                    self.help()

    # Update the cells state
    def update(self):
        self.m_CA.update()

    #render
    def render(self):
        self.m_Clock.tick(self.m_FPS)
        self.m_Display.fill((0, 0, 0))


        if self.m_ShowLattice:
            #Lines of lattice
            for j in range(1, self.m_CA.getHeight()):
                pygame.draw.line(self.m_Display, (0, 255, 0), (0, j * self.m_DY), (self.m_Width, j * self.m_DY))

            #columns of lattice
            for i in range(1, self.m_CA.getWidth()):
                pygame.draw.line(self.m_Display, (0, 255, 0), (i * self.m_DX, 0), (i * self.m_DX, self.m_Height))


        #state render only if s > 0. 0 state is black
        for j in range(0, self.m_CA.getHeight()):
            for i in range(0, self.m_CA.getWidth()):
                s = self.m_CA.getState(j, i)

                if s > 0:
                    c = s % len (self.m_Palettes)
                    color = self.m_Palettes[c]
                    x = i * self.m_DX
                    y = j * self.m_DY
                    pygame.draw.rect(self.m_Display, (color.r, color.g, color.b), (x + 1, y + 1, self.m_DX - 2, self.m_DY - 2), 0)
        pygame.display.flip()

    def toPNG(self):
        s = self.m_CA.getTimeStep()
        filename = 'snapshot-{}.png'.format(s)
        pygame.image.save(self.m_Display, filename)
        print('File: ', filename, ' saved')

    def help(self):
        print('GUI commands help:')
        print('\t ESC - close window')
        print('\t e - Step by step on/off')
        print('\t h - show this help')
        print('\t l - show on/off lattice')
        print('\t u - update the CA states')
        print('\t s - save CA snapshot in PNG format')

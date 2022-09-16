    ################################################################################
#

#
#  Universidade Federal Fluminense - Medialab
#  por: Marcelo Zamith - mzamith@ic.uff.br
#  para compilar com target release use o comando: make TARGET=release
#  -framework Cocoa
#
################################################################################
EXEFILE     = CA.bin
VERSION     = -D_VERSION=\"0.01\"
APPLICATION = -D_APPLICATION=\"$(EXEFILE)\"
CPUCC     = g++
CPPFLAGS  = -g
DEFS      = 

INCLUDES  = -I.                           \
            -I/opt/glew/include \
            -I/usr/include/GL

LIBDIR   =  -L/usr/lib                          
 

LIBS     =   -lm  -lGLEW -lGLU -lglut -lGL 

LINK     =  $(LIBDIR) $(LIBS)

C_COMPILE = $(CPUCC) $(DEFS) $(INCLUDES) $(CPPFLAGS) 


all:   CellularAutomata main  
	$(C_COMPILE) obj/CellularAutomata.o obj/main.o    $(LINK) -o $(EXEFILE)

main:
	$(C_COMPILE) -c main.cpp -o obj/main.o
    
CellularAutomata:
	$(C_COMPILE) -c CellularAutomata.cpp -o obj/CellularAutomata.o


clean:
	rm obj/*.o; rm $(EXEFILE)

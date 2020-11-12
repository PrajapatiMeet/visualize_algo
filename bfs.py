import pygame
from queue import Queue
import random

# initialize pygame
pygame.init()

# assign parameters
width = 1005                    # width of display
height = 600                    # height of display
gap = 15                        # size of squere node
rows = height // gap            # number of total rows 
cols = width // gap             # number of total columns
start_node = None               # start node
end_node = None                 # target node
q = Queue()                     # for depth first search
begin = False                   # for visualize searching
visualize = False               # for visualize path
path = None                     

# colors
RED = (255, 0, 0)               # represent target node
GREEN = (0, 255, 0)             # represent visited nodes
BLUE = (0, 0, 255)              # represent end node
WHITE = (255, 255, 255)         # represent free nodes
BLACK = (0, 0, 0)               # for grid lines
GREY = (50, 50, 50)             # represent wall 
YELLOW = (255, 255, 0)          # represent path

# node class 
class node:
    def __init__(self, x, y):
        self.x = x                  # row number in grid
        self.y = y                  # column nuber in grid
        self.color = WHITE          # state of node
        self.neighbours = []        # neighbours of node
        self.come_from = None       # previous node

    # functions for check state of node
    def isFree(self):
        return self.color == WHITE

    def isVisited(self):
        return self.color == GREEN

    def isStart(self):
        return self.color == BLUE

    def isEnd(self):
        return self.color == RED

    def isWall(self):
        return self.color == GREY

    def isPath(self):
        return self.color == YELLOW

    # functions for change state of node
    def makeFree(self):
        self.color = WHITE
    
    def makeVisisted(self):
        self.color = GREEN

    def makeStart(self):
        self.color = BLUE
    
    def makeEnd(self):
        self.color = RED
    
    def makeWall(self):
        self.color = GREY
    
    def makePath(self):
        self.color = YELLOW

# make graph
grid = []
for i in range(rows):
    grid.append([])
    for j in range(cols):
        grid[i].append(node(i, j))

# assign neighbours
def make_neighs():
    for i in range(rows):
        for j in range(cols):
            n = grid[i][j]
            n.neighbours = []

            if i != 0 and not grid[i-1][j].isWall():
                n.neighbours.append(grid[i-1][j])
            
            if j != 0 and not grid[i][j-1].isWall():
                n.neighbours.append(grid[i][j-1])
            
            if i != rows-1 and not grid[i+1][j].isWall():
                n.neighbours.append(grid[i+1][j])
            
            if j != cols-1 and not grid[i][j+1].isWall():
                n.neighbours.append(grid[i][j+1])

# draw grid    
def draw_grid():
    for i in range(rows):
        pygame.draw.line(screen, BLACK, (0, i*gap), (width, i*gap))
        pygame.draw.line(screen, BLACK, (i*gap, 0), (i*gap, height))
    for i in range(rows, cols):
        pygame.draw.line(screen, BLACK, (i*gap, 0), (i*gap, height))

# draw nodes
def draw_nodes():
    for i in range(rows):
        for j in range(cols):
            pygame.draw.rect(screen, grid[i][j].color, (j*gap, i*gap, gap, gap))

# make random walls
def make_wall():
    for i in range(1000):
        r = random.randint(0, 39)
        c = random.randint(0, 66)
        grid[r][c].makeWall()

# reset 
def reset():
    for i in range(rows):
        for j in range(cols):
            grid[i][j].makeFree()

# make screen
screen = pygame.display.set_mode((width, height))

# main loop
running = True
while running:
    for event in pygame.event.get():

        # for quit
        if event.type == pygame.QUIT:
            running = False

        if begin or visualize:
            continue
        
        # keyboard inputs
        if event.type == pygame.KEYDOWN:

            # input for start visualize
            if event.key == pygame.K_SPACE:
                if not start_node is None and not end_node is None:
                    q.put(start_node)
                    begin = True
            
            # input for make random walls
            if event.key == pygame.K_w:
                make_wall()
        
        # input for left click of mouse
        if pygame.mouse.get_pressed()[0]:

            # calculate row and column number
            pos = pygame.mouse.get_pos()
            row = pos[1] // gap
            col = pos[0] // gap
            n = grid[row][col]
             
            # make start node
            if start_node is None:
                start_node = n
                start_node.makeStart()

            # make end node
            elif end_node is None:
                if n is start_node:
                    start_node = None
                end_node = n
                end_node.makeEnd()
            
            # make wall
            else:
                if n is start_node:
                    start_node = None
                if n is end_node:
                    end_node = None
                n.makeWall()
        
        # mouse input for right click
        if pygame.mouse.get_pressed()[2]:

            # calculate row and column number
            pos = pygame.mouse.get_pos()
            row = pos[1] // gap
            col = pos[0] // gap
            n = grid[row][col]
            
            if n is start_node:         # check for start_node
                start_node = None

            if n is end_node:           # check for end_node
                end_node = None
            
            # make state of node free 
            n.makeFree()

    # visualize searching
    if begin: 
        if q.empty():                           # check if queue is empty 
            key = pygame.key.get_pressed()      # take input for reset       
            if key[pygame.K_r]:                 
                reset()
                q = Queue()
                begin = False
            continue

        # breath first search   
        current = q.get()
        current.makeVisisted()
        for n in current.neighbours:
            if not n.isVisited():
                n.makeVisisted()
                n.come_from = current
                q.put(n)

        # check if end_node is visited
        if end_node.isVisited():
            begin = False
            visualize = True
            path = end_node

    # visualize path
    if visualize:

        # check if completed
        if path is start_node:           
            key = pygame.key.get_pressed()      # take input for reset
            if key[pygame.K_r]:
                reset()
                q = Queue()
                visualize = False
        
        # continue visualizing if not completed
        else:
            path = path.come_from
        path.makePath()
    
    # changes for every frame
    if not start_node is None:      # start_node
        start_node.makeStart()
    if not end_node is None:        # end_node
        end_node.makeEnd()

    make_neighs()                   # assign neighbours 
    screen.fill(WHITE)              # fill white color
    draw_nodes()                    # draw nodes
    draw_grid()                     # draw lines for grid
    pygame.display.update()         # update display
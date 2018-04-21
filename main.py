import pygame
import random

pygame.init()
win_wd = 400
win_hg = 300
screen = pygame.display.set_mode((win_wd, win_hg))
pygame.display.set_caption("A Nice Game")
done = False

done = False
is_blue = True
x = 30
y = 30

clock = pygame.time.Clock()

class Cell:
    def __init__(self, color, grid, pos):
        self.color = color
        self.grid = grid
        self.pos = pos

    def __repr__(self):
        return str(self.color)



class CellGrid:

    colors = [(60, 128, 255), (128, 200, 40), (224, 20, 28), (0,0,0), (255,255,255)]

    def __init__(self, colornb, width, height, screen):
        self.colornb = colornb
        self.width = width
        self.height = height
        self.screen = screen
        self.cell_height =  int(win_hg / height)
        self.cell_width = int(win_wd / width)
        self.grid = []
        for y in range(height):
            row = []
            for x in range(width):
                color = random.randrange(colornb)
                row.append(Cell(color, self.grid, (x * self.cell_width, y * self.cell_height)))
            self.grid.append(row)
        self.update_dict = self.update_rule()
        print(self.update_dict)

    def child_choice(self, mode, nbhood):
        if mode == 0:
            return random.randrange(self.colornb)
        if mode == 1:
            max_char = '0'
            max_count = nbhood.count('0')
            for i in "1234":
                if nbhood.count(i) > max_count:
                    max_count = nbhood.count(i)
                    max_char = i
            return int(max_char)

    def update_rule(self):
        dict = {}
        colors = "01234"
        for keys in range(pow(self.colornb, 5)):
            s = list("     ")
            for i in range(self.colornb):
                s[0] = colors[i]
                for j in range(self.colornb):
                    s[1] = colors[j]
                    for k in range(self.colornb):
                        s[2] = colors[k]
                        for l in range(self.colornb):
                            s[3] = colors[l]
                            for m in range(self.colornb):
                                s[4] = colors[m]
                                res = "".join(s)
                                dict[res] = self.child_choice(1, res)
        return dict

    def update(self):
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                s = ""
                nx = 0 if x + 1 == self.width  else x+1
                ny = 0 if y + 1 == self.height else y+1
                #order in heredity string is center, north, south, west, east. The 2D plane loops at the borders.
                s = s + str(self.grid[y  ][x  ].color)
                s = s + str(self.grid[y-1][x  ].color)
                s = s + str(self.grid[ny ][x  ].color)
                s = s + str(self.grid[y  ][x-1].color)
                s = s + str(self.grid[y  ][nx ].color)
                color = self.update_dict[s]
                row.append(Cell(color, self.grid, (x * self.cell_width, y * self.cell_height)))
            grid.append(row)
        self.grid = grid

    def display(self):
        print(self.grid)
        for row in self.grid:
            for cell in row:
                #print(cell.pos)
                #print((self.cell_width, self.cell_height))
                pygame.draw.rect(self.screen, self.colors[cell.color],
                                 pygame.Rect(cell.pos, (self.cell_width, self.cell_height)))



grid = CellGrid(3, 80, 60, screen)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    screen.fill((0, 0, 0))
    grid.display()
    pygame.display.flip()
    grid.update()
    clock.tick(5)
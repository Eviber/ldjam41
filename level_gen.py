import pygame
import random
import copy

pygame.init()
win_wd = 1600
win_hg = 1200
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

    def __eq__(self, other):
        return self.color == other.color


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

        elif mode == 1 or mode == 2:
            max_char = '0'
            max_count = nbhood.count('0')
            for i in "1234":
                if nbhood.count(i) > max_count:
                    max_count = nbhood.count(i)
                    max_char = i
                elif nbhood.count(i) == max_count and mode == 2:
                    if random.randrange(2):
                        max_count = nbhood.count(i)
                        max_char = i
            return int(max_char)

        elif 3 <= mode:
            counts = [nbhood.count(x) for x in "01234"]
            maxint = counts.index(max(counts))
            vrand = random.randrange(2)
            #print(str(counts) + " __ " + str(maxint) + " __ " + str(vrand))
            if mode == 3:
                for i in range(self.colornb - 1):
                    for j in range(i + 1, self.colornb):
                        if counts[i] == counts[j]:
                            if i == maxint or j == maxint:
                                return maxint
                            else:
                                return i if vrand else j
                return maxint
            if mode == 4:
                return self.colornb - maxint - 1




    def update_rule(self):
        mode = 3
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
                                dict[res] = self.child_choice(mode, res)
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
        #print(self.grid)
        for row in self.grid:
            for cell in row:
                #print(cell.pos)
                #print((self.cell_width, self.cell_height))
                pygame.draw.rect(self.screen, self.colors[cell.color],
                                 pygame.Rect(cell.pos, (self.cell_width, self.cell_height)))

    def clean(self, boolgrid):
        #boolgrid should be false on unstable spots
        for y in range(self.height):
            for x in range(self.width):
                if not boolgrid[y][x]:
                    self.grid[y][x] = Cell(0, self.grid, (x, y))

    def __eq__(self, other):
        if self.width != other.width or self.height != other.height:
            return False
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x] != other.grid[y][x]:
                    return False
        return True

    def __and__(self, other):
        return [[self.grid[y][x] == other.grid[y][x] for x in range(self.width)] for y in range(self.height)]

    def __str__(self):
        s = ""
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += str(self.grid[y][x])
            row = "\"" + row + "\",\n"
            s += row
        return s


random.seed(4201337)

grid = CellGrid(2, 160, 120, screen)
print(grid)
gparent = copy.copy(grid)
grid.update()
print(grid)
parent = copy.copy(grid)


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))
    grid.display()
    pygame.display.flip()
    grid.update()
    print(gparent)
    print(grid)
    if grid == gparent:
        unstables = gparent & parent
        grid.clean(unstables)
        print(grid)
        break
    else:
        gparent = copy.copy(parent)
        parent = copy.copy(grid)
    clock.tick(5)
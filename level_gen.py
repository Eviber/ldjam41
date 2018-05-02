import pygame
import random
import copy


class Cell:
    def __init__(self, color, grid, pos):
        self.color = color
        self.grid = grid
        self.pos = pos

    def __repr__(self):
        return str(self.color)

    def __eq__(self, other):
        if isinstance(other, int):
            return self.color == other
        else:
            return self.color == other.color

    def __int__(self):
        return self.color


class CellularAutomata:

    colors = [(60, 128, 255), (128, 200, 40), (224, 20, 28), (0, 0, 0), (255, 255, 255)]
    viridis = [(200, 200, 200),
               (68, 1, 84),    (69, 55, 129),  (35, 138, 141),
               (31, 150, 139), (41, 175, 127), (85, 198, 103),
               (115, 208, 85), (184, 222, 41), (253, 231, 37)]

    cell_width = 3
    cell_height = 3

    def __init__(self, colornb, width, height, screen, seed=None):
        self.colornb = colornb
        self.width = width      #number of cells
        self.height = height
        self.screen = screen
        self.grid = []
        if seed is None:
            for y in range(height):
                row = []
                for x in range(width):
                    color = random.randrange(colornb)
                    row.append(Cell(color, self.grid, (x, y)))
                self.grid.append(row)
        else:
            self.update_grid_with_strls(seed)
        self.update_dict = self.update_rule()
        #print(self.update_dict)

    def inbounds(self, point):
        return (0 <= point[0] and point[0] <= self.width and
                0 <= point[1] and point[1] <= self.height)

    def update_grid_with_strls(self, sl):
        height = len(sl)
        width = len(sl[0])
        self.grid = [[Cell(int(sl[y][x]), self.grid, (x, y)) for x in range(width)] for y in range(height)]
        self.height = height
        self.width = width

    def child_choice(self, mode, nbhood):

        #modes after this line use rank 0 nbhood

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

        #2 colors gives great level generation for this one
        elif mode == 3:
            counts = [nbhood.count(x) for x in "01234"]
            maxint = counts.index(max(counts))
            vrand = random.randrange(2)
            #print(str(counts) + " __ " + str(maxint) + " __ " + str(vrand))
            for i in range(self.colornb - 1):
                for j in range(i + 1, self.colornb):
                    if counts[i] == counts[j]:
                        if i == maxint or j == maxint:
                            return maxint
                        else:
                            return i if vrand else j
                return maxint

        #not very interesting level design wise, but cute with 4 colors
        elif mode == 4:
            card = nbhood[1:self.colornb]
            counts = [card.count(x) for x in "01234"]
            for i in range(3):
                for j in range(1, 4):
                    if counts[i] == counts[j] and abs(i-j) == 1:
                        return int(nbhood[i])
            return int(card[max(counts)])

        #fun with 2 colors, maybe of interest
        elif mode == 5:
            vrand = random.randrange(5)
            if vrand == 0:
                return self.child_choice(0, nbhood)
            elif vrand == 1:
                return self.child_choice(4, nbhood)
            else:
                return self.child_choice(3, nbhood)

        #pretty nice with 2 colors
        elif mode == 6:
            vrand = random.randrange(5)
            if vrand == 0:
                return self.child_choice(2, nbhood)
            elif vrand == 1:
                return self.child_choice(4, nbhood)
            else:
                return self.child_choice(3, nbhood)

        elif mode == 7:
            b = False
            counts = [nbhood.count(x) for x in "01234"]
            maxint = counts.index(max(counts))

            s = nbhood[3] + nbhood[0] + nbhood[4] #left, center, right
            if s == "000" or s == "010" or s == "001":
                return 0
            elif s == "110" or s == "011":
                b = True
            elif s == "101":
                return 1

            s = nbhood[1] + nbhood[0] + nbhood[2] #up, center, down
            if s == "000" or s == "010" or s == "001":
                return maxint * (1 - b)
            elif s == "101":
                return 0

            return self.child_choice(3, nbhood)

        # modes after this line use rank 1 nbhood

        # the following mode is rank 0 and is used for spritesheet definition; "SPRITE"
        elif mode == "SPRITE1":
            if nbhood[0] == '0':
                return 0
            else:
                s = nbhood[1:5]
                if s == "0101" or s == "0111" or s == "0110" or s == "1101" or s == "1111" or s == "1110" or s == "1001" or s == "1011" or s == "1010" or s == "1001" or s == "0110":
                    return 1
                else:
                    return 0
        elif mode == "SPRITE2":
            s = nbhood[1:5]
            if nbhood[0] == '0':
                return 0
            elif s == "0101":
                return 1
            elif s == "0111":
                return 2
            elif s == "0110":
                return 3
            elif s == "1101":
                return 4
            elif s == "1111":
                return 5
            elif s == "1110":
                return 6
            elif s == "1001":
                return 7
            elif s == "1011":
                return 8
            elif s == "1010":
                return 9
            else:
                return 0

    def update_rule(self, mode=None):
        if mode is None:
            mode = 7
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

    def get_nbhood(self, x, y, rank):
        #rank == 0 => manhattan nbhood, dist 1 ; rank == 1 => square nbh, dist 1
        s = ""
        nx = 0 if x + 1 == self.width else x + 1
        ny = 0 if y + 1 == self.height else y + 1
        # order in heredity string is center, north, south, west, east. The 2D plane loops at the borders.
        if rank == 0:
            s = s + str(self.grid[y    ][x    ].color)
            s = s + str(self.grid[y - 1][x    ].color)
            s = s + str(self.grid[ny   ][x    ].color)
            s = s + str(self.grid[y    ][x - 1].color)
            s = s + str(self.grid[y    ][nx   ].color)
        # order is lexicographic (left right then top down)
        elif rank == 1:
            s = s + str(self.grid[y - 1][x - 1].color)
            s = s + str(self.grid[y - 1][x    ].color)
            s = s + str(self.grid[y - 1][nx   ].color)
            s = s + str(self.grid[y    ][x - 1].color)
            s = s + str(self.grid[y    ][x    ].color)
            s = s + str(self.grid[y    ][nx   ].color)
            s = s + str(self.grid[ny   ][x - 1].color)
            s = s + str(self.grid[ny   ][x    ].color)
            s = s + str(self.grid[ny   ][nx   ].color)
        return s

    def update(self, rank=0, mode=None):
        dict = self.update_dict if mode is None else self.update_rule(mode=mode)
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                s = self.get_nbhood(x, y, rank)
                color = dict[s]
                row.append(Cell(color, self.grid, (x, y)))
            grid.append(row)
        self.grid = grid

    def build_minimap(self, spawn_n_goal, mode=None, dim=None):
        colorarr = self.colors if mode is None else self.viridis
        minimap = pygame.Surface((self.width * self.cell_width, self.height * self.cell_height))
        """
        #print("DEBUG DISPLAY")
        #print(self.grid[2][2])
        #print(self.cell_width)
        #print(self.cell_height)
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                pygame.draw.rect(self.screen,
                                 colorarr[cell.color],
                                 pygame.Rect((cell.pos[0], cell.pos[1]),
                                             (self.cell_width, self.cell_height)))
        """
        for y in range(self.height):
            for x in range(self.width):
                if (x,y) == spawn_n_goal[0]:
                    color = (0, 0, 0)
                elif (x,y) == spawn_n_goal[1]:
                    color = (255, 255, 255)
                else:
                    color = colorarr[self.grid[y][x].color]
                for px in range(self.cell_height):
                    for py in range(self.cell_width):
                        minimap.set_at((x * self.cell_width + px, y * self.cell_height + py), color)
        return minimap


    def clean(self, boolgrid):
        #boolgrid should be false on unstable spots
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                if not boolgrid[y][x]:
                    row.append(Cell(0, grid, (x,y)))
                else:
                    row.append(copy.copy(self.grid[y][x]))
            grid.append(row)
        self.grid = grid


    def scale3x(self):
        """
        source wikipedia pixel scaling algorithms
        """
        tiles_9by9 = []
        for y in range(self.height):
            for x in range(self.width):
                s = self.get_nbhood(x, y, 1)
                c = s[4]
                lc = [c, c, c, c, c, c, c, c, c]
                if s[3] == s[1] and s[3] != s[7] and s[1] != s[5]:
                    lc[0] = s[3]
                if (s[3] == s[1] and s[3] != s[7] and s[1] != s[5] and c != s[2]) or (s[1] == s[5] and s[1] != s[3] and s[5] != s[7] and c != s[0]):
                    lc[1] = s[1]
                if s[1] == s[5] and s[1] != s[3] and s[5] != s[7]:
                    lc[2] = s[5]
                if (s[7] == s[3] and s[7] != s[5] and s[3] != s[1] and c != s[0]) or (s[3] == s[1] and s[3] != s[7] and s[1] != s[5] and c != s[6]):
                    lc[3] = s[3]
                    #sl[4] = c
                if (s[1] == s[5] and s[1] != s[3] and s[5] != s[7] and c != s[8]) or (s[5] == s[7] and s[5] != s[1] and s[7] != s[3] and c != s[2]):
                    lc[5] = s[5]
                if s[7] == s[3] and s[7] != s[5] and s[3] != s[1]:
                    lc[6] = s[3]
                if (s[5] == s[7] and s[5] != s[1] and s[7] != s[3] and c != s[6]) or (s[7] == s[3] and s[7] != s[5] and s[3] != s[1] and c != s[8]):
                    lc[7] = s[7]
                if s[5] == s[7] and s[5] != s[1] and s[7] != s[3]:
                    lc[8] = s[5]
                tiles_9by9.append("".join(lc))
        sl = []
        for y in range(self.height):
            row = ""
            start = (y % 3) * 3
            for x in range(self.width):
                row += tiles_9by9[y * self.width + x][start:start+3]
            sl.append(row)
        self.update_grid_with_strls(sl)


    def floodfill(self):

        areas = copy.copy(self.grid)

        def flood_fill(cellgrid, x, y, areanb):
            acc = 0
            if cellgrid[y][x].color == 0:
                acc = 1
                cellgrid[y][x].color = areanb
                if x > 0:
                    acc += flood_fill(cellgrid, x - 1, y, areanb)
                if x < len(cellgrid[y]) - 1:
                    acc += flood_fill(cellgrid, x + 1, y, areanb)
                if y > 0:
                    acc += flood_fill(cellgrid, x, y - 1, areanb)
                if y < len(cellgrid) - 1:
                    acc += flood_fill(cellgrid, x, y + 1, areanb)
            return acc

        areanb = 2
        cellnb_per_area = []
        for y in range(self.height):
            for x in range(self.width):
                if areas[y][x].color == 0:
                    cellnb_per_area.append(flood_fill(areas, x, y, areanb))
                    areanb += 1
        nb_maxarea = 2 + cellnb_per_area.index(max(cellnb_per_area))

        for y in range(self.height):
            for x in range(self.width):
                areas[y][x].color = 0 if areas[y][x].color == nb_maxarea else 1
        #print(areas)
        self.grid = areas


    def build_spawnpos_and_goalpos(self):
        #heatmaps = disttoobst foreach (x,y)
        #heatpoints = list of topological maxima in discrete manifold/"heat mountaintops"

        heatmap = [[0 for x in range(self.width)] for y in range(self.height)]

        def dist_to_obst(x, y, map):
            if map[y][x] == 1:
                return 0
            def circle_of_manhattan_radius_n(map, center, n):
                points = []
                for orient in range(4): #building the points in the trigonometric order
                    iter = (0,0)
                    start = (0,0)
                    if orient == 0:     #east
                        start = (x + n, y    )
                        iter = (-1, -1)
                    elif orient == 1:   #north
                        start = (x    , y - n)
                        iter = (-1,  1)
                    elif orient == 2:   #west
                        start = (x - n, y    )
                        iter = ( 1,  1)
                    else:               #south
                        start = (x    , y + n)
                        iter = ( 1, -1)
                    for i in range(n):
                        if self.inbounds(start):
                            points.append(start)
                        start = (start[0] + iter[0], start[1] + iter[1])
                return points
            d2o = -1
            tmpd2o = 1
            while d2o == -1:
                points = circle_of_manhattan_radius_n(map, (x, y), tmpd2o)
                #print(points)
                for p in points:
                    if map[p[1]][p[0]] == 1:
                        d2o = tmpd2o
                        break
                tmpd2o += 1
            return d2o

        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].color == 0:
                    heatmap[y][x] = dist_to_obst(x, y, self.grid)

        #print("heatmap:")
        #for row in heatmap:
        #    print(("".join(["\t" + str(x) for x in row])) + ",")

        heatlist = []
        for row in heatmap:
            for col in row:
                heatlist.append(col)

        #print("heat list : ", heatlist)

        seen = []
        for i in heatlist:
            if not i in seen:
                seen.append(i)
        seen.sort()

        #print(seen)

        heatpoints = []
        maxval = seen[-1]
        for y in range(self.height):
            for x in range(self.width):
                if i < 0:
                    break
                if heatmap[y][x] == maxval:
                    heatpoints.append((x, y))
                    heatmap[y][x] = -heatmap[y][x]

        #print("heatmap:")
        #for row in heatmap:
        #    print("".join(["\t" + str(x) for x in row]), ",")

        #print("heatpoints")
        #print(heatpoints)

        x, y = random.choice(heatpoints)
        while self.grid[y+1][x].color != 1:
            y += 1

        goalpos = (x, y)

        distmap = self.build_manhattan_distance_map(x, y)
        maxdist = 0
        maxp = (0,0)
        for y in range(self.height):
            for x in range(self.width):
                if distmap[y][x] >= maxdist:
                    maxdist = distmap[y][x]
                    maxp = (x,y)

        while self.grid[maxp[1]+1][maxp[0]].color != 1:
            maxp = (maxp[0], maxp[1] + 1)

        self.grid[maxp[1] - 1][maxp[0] - 1].color = 0
        self.grid[maxp[1] - 1][maxp[0]    ].color = 0
        self.grid[maxp[1] - 1][maxp[0] + 1].color = 0
        self.grid[maxp[1]    ][maxp[0] - 1].color = 0
        self.grid[maxp[1]    ][maxp[0] + 1].color = 0

        return maxp, goalpos


    def build_manhattan_distance_map(self, x, y):
        #returns a manhattan distance heatmap with obstacles
        k = 0
        kmax = 1
        distmap_center_xy = [[-1 for x in range(self.width)] for y in range(self.height)]
        distmap_center_xy[y][x] = 0
        while k <= kmax:
            for y in range(self.height):
                for x in range(self.width):
                    if distmap_center_xy[y][x] == k:
                        if  y     != 0 and distmap_center_xy[y-1][x] == -1 and self.grid[y - 1][x] == 0:
                            distmap_center_xy[y-1][x] = k+1
                        if  y + 1 != self.height and distmap_center_xy[y + 1][x] == -1 and self.grid[y + 1][x] == 0:
                            distmap_center_xy[y+1][x] = k+1
                        if  x     != 0 and distmap_center_xy[y][x-1] == -1 and self.grid[y][x - 1] == 0:
                            distmap_center_xy[y][x-1] = k+1
                        if  x + 1 != self.width and distmap_center_xy[y][x + 1] == -1 and self.grid[y][x + 1] == 0:
                            distmap_center_xy[y][x+1] = k+1
                        kmax = k+1
            k += 1
        #print("Manhattan map centered in " + str((x, y)))
        #print(distmap_center_xy)
        return distmap_center_xy



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

    def __or__(self, other):
        return [[self.grid[y][x].color == 1 or other.grid[y][x].color == 1 for x in range(self.width)] for y in range(self.height)]

    def __str__(self):
        s = ""
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                row += str(self.grid[y][x])
            row = "\"" + row + "\",\n"
            s += row
        return s



def gen_walltemplate(x, y):
    res = []
    s = "".join(['1' for i in range(x)])
    s2 = "11" + "".join(['0' for i in range(x - 4)]) + "11"
    res.append(s)
    res.append(s)
    res.append(s)
    for i in range(y-7):
        res.append(s2)
    res.append(s)
    res.append(s)
    res.append(s)
    res.append(s)
    return res


def map_gen(screen, mapsize=(400,300), seed=4201337):
    #full map's size in pixels, the camera will show a portion
    random.seed(seed)
    colornb = 2
    print("mapsize")
    print(mapsize)
    x_cells = int(mapsize[0] / 10)
    y_cells = int(mapsize[1] / 10)

    #grid is first a strls then a CellGrid
    walltemplate = gen_walltemplate(x_cells, y_cells)
    grid = CellularAutomata(colornb, x_cells, y_cells, screen) | CellularAutomata(colornb, x_cells, y_cells, screen, seed=walltemplate)
    grid = CellularAutomata(colornb, x_cells, y_cells, screen, seed=grid)
    #print(grid)
    gparent = copy.copy(grid)


    grid.update()
    #print(grid)
    parent = copy.copy(grid)

    i = 0
    status = 0
    done = False
    spawnpos_n_goalpos_2tup = ((0,0),(0,0))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pygame.display.flip()
        if status == 0:
            grid.update()
            #print(grid)
            if grid == gparent or i == 100:
                unstables = gparent & parent
                grid.clean(unstables)
                #print(grid)
                status = 1
            else:
                gparent = copy.copy(parent)
                parent = copy.copy(grid)
        if status == 1:
            #tmp = zeros(grid.width, grid.height)
            #loots = grid.get_areas
            grid.floodfill()
            print(grid)
            grid.scale3x()
            print(grid)
            spawnpos_n_goalpos_2tup = grid.build_spawnpos_and_goalpos()
            print(spawnpos_n_goalpos_2tup)
            grid.update(mode="SPRITE1")
            grid.update(mode="SPRITE2")
#            print(grid)
            done = 1
        i += 1

    minimap = grid.build_minimap(spawnpos_n_goalpos_2tup, mode="SPRITE")
    return grid.grid, spawnpos_n_goalpos_2tup, minimap

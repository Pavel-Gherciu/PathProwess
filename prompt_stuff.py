import random

import pygame
import pygame_gui
import math
from queue import PriorityQueue
import algorithms

WIN_WIDTH = 1000
GRID_WIDTH = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_WIDTH))
GRID_SURFACE = pygame.Surface((GRID_WIDTH, GRID_WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, start):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
        if current != start:
            current.make_path()
        draw()
    return len(path)


# astar

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw, start)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
    pygame.draw.line(win, GREY, (0, width - 1), (width, width - 1))  # Bottom line
    pygame.draw.line(win, GREY, (width - 1, 0), (width - 1, width))  # Right line


def draw(win, grid, rows, width):
    GRID_SURFACE.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(GRID_SURFACE)

    draw_grid(GRID_SURFACE, rows, width)

    # Draw the grid surface onto the window
    win.blit(GRID_SURFACE, ((WIN_WIDTH - GRID_WIDTH) // 2, (WIN_WIDTH - GRID_WIDTH) // 2))
    #win.blit(GRID_SURFACE, ((0, 50)))
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = GRID_WIDTH // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def reset_grid(grid, start, end):
    for row in grid:
        for spot in row:
            if spot != start and spot != end and not spot.is_barrier():
                spot.reset()


def main(win, width):
    ROWS = 10
    grid = make_grid(ROWS, GRID_WIDTH)

    start = None
    end = None

    dragging_start = False
    dragging_end = False

    prev_start_spot = None
    prev_end_spot = None


    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            pos = pygame.mouse.get_pos()
            pos = (pos[0] - (WIN_WIDTH - GRID_WIDTH) // 2, pos[1] - (WIN_WIDTH - GRID_WIDTH) // 2)
            on_grid = 0 <= pos[0] < GRID_WIDTH and 0 <= pos[1] < GRID_WIDTH

            if on_grid:
                row, col = get_clicked_pos(pos, ROWS, width)
                if row < len(grid) and col < len(grid[0]):
                    spot = grid[row][col]

            if pygame.mouse.get_pressed()[0]:  # LEFT
                if on_grid:
                    if not start and spot != end and not dragging_end and not spot.is_barrier():
                        start = spot
                        start.make_start()
                        dragging_start = True

                    elif not end and spot != start and not dragging_start and not spot.is_barrier():
                        end = spot
                        end.make_end()
                        dragging_end = True

                    elif spot != end and spot != start and not dragging_start and not dragging_end:
                        spot.make_barrier()

                    if spot == start:
                        dragging_start = True

                    if spot == end:
                        dragging_end = True

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                if on_grid:
                    spot.reset()
                    if spot == start:
                        start = None
                        dragging_start = False
                    elif spot == end:
                        end = None
                        dragging_end = False

            if event.type == pygame.MOUSEBUTTONUP:
                dragging_start = False
                dragging_end = False
                prev_start_spot = None
                prev_end_spot = None

            if dragging_start and on_grid and spot != end and not spot.is_barrier():
                if prev_start_spot:
                    prev_start_spot.reset()
                prev_start_spot = spot
                start.reset()
                start = spot
                start.make_start()

            if dragging_end and on_grid and spot != start and not spot.is_barrier():
                if prev_end_spot:
                    prev_end_spot.reset()
                prev_end_spot = spot
                end.reset()
                end = spot
                end.make_end()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    reset_grid(grid, start, end)  # Reset the grid before running the algorithm
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, GRID_WIDTH)

import pygame
import pygame_gui
import math
from queue import PriorityQueue

from pygame_gui.windows import UIColourPickerDialog

import algorithms
import random
from enum import Enum, auto
from math import sin
import time
import json

import settings


pygame.init()
screen_info = pygame.display.Info()
SHOW_ARROWS = settings.SHOW_ARROWS
SHOW_COORDS = settings.SHOW_COORDS
GRID1 = settings.GRID1
GRID2 = settings.GRID2
GRID3 = settings.GRID3
GRID4 = settings.GRID4
DARK_MODE = settings.DARK_MODE
DIAGONAL = settings.DIAGONAL
mode = settings.mode

RECORDING = False

chosen_heuristic = algorithms.heuristic(algorithms.Heuristic.EUCLIDEAN)


WIN_WIDTH = 1000
GRID_WIDTH = 900
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
pygame.font.init()
pygame.display.set_caption("PathProwess")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (60, 63, 65)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (220, 220, 220)
TURQUOISE = (64, 224, 208)
BG_COLOR = (0, 0, 0)

DARK_BG = "#3C3F41"


from ui_elements import *
from ui_windows import *
from plots import *


GRID_SURFACE = pygame.Surface((GRID_WIDTH, GRID_WIDTH))

GRID_WIDTH2 = 500

GRID_WIDTH3 = 400

GRID_WIDTH4 = 400

GRID_SURFACE2_1 = pygame.Surface((GRID_WIDTH2, GRID_WIDTH2))
GRID_SURFACE2_2 = pygame.Surface((GRID_WIDTH2, GRID_WIDTH2))

GRID_SURFACE3_1 = pygame.Surface((GRID_WIDTH3, GRID_WIDTH3))
GRID_SURFACE3_2 = pygame.Surface((GRID_WIDTH3, GRID_WIDTH3))
GRID_SURFACE3_3 = pygame.Surface((GRID_WIDTH3, GRID_WIDTH3))

GRID_SURFACE4_1 = pygame.Surface((GRID_WIDTH4, GRID_WIDTH4))
GRID_SURFACE4_2 = pygame.Surface((GRID_WIDTH4, GRID_WIDTH4))
GRID_SURFACE4_3 = pygame.Surface((GRID_WIDTH4, GRID_WIDTH4))
GRID_SURFACE4_4 = pygame.Surface((GRID_WIDTH4, GRID_WIDTH4))



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
        self.predecessor = None  # Add this line
        self.arrow_color = None  # Add this line

        # Cache the text surfaces for the coordinates
        font = pygame.font.Font(None, int(self.width * 0.4))
        self.x_text = font.render(f"{self.row}", True, GREY)
        self.y_text = font.render(f"{self.col}", True, GREY)

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
        self.update_arrow()

    def make_start(self):
        self.color = ORANGE
        self.update_arrow()

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK
        self.update_arrow()

    def make_end(self):
        self.color = TURQUOISE
        self.update_arrow()

    def make_path(self):
        self.color = PURPLE

    def draw(self, win, time_elapsed=None, algorithm_completed=False):

        # colorarea end point
        if self.is_end() and time_elapsed is not None and algorithm_completed:
            pulse_amplitude = 100
            pulse_speed = 10
            pulse_offset = 155
            pulse_color = int(pulse_amplitude * sin(pulse_speed * time_elapsed) + pulse_offset)
            if mode == "square":
                pygame.draw.rect(win, (64, 224, pulse_color), (self.x, self.y, self.width, self.width))
            elif mode == "hexagon":
                hex_points = self.get_hexagon_points()
                pygame.draw.polygon(win, (64, 224, pulse_color), hex_points)
            elif mode == "triangle":
                tri_points = self.get_triangle_points()
                pygame.draw.polygon(win, (64, 224, pulse_color), tri_points)
        else:
            #colorarea principala
            if mode == "square":
                pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
            elif mode == "hexagon":
                hex_points = self.get_hexagon_points()
                pygame.draw.polygon(win, self.color, hex_points)
            elif mode == "triangle":
                tri_points = self.get_triangle_points()
                pygame.draw.polygon(win, self.color, tri_points)

        # pentru coordonate
        if SHOW_COORDS:
            x_text_rect = self.x_text.get_rect(topleft=(self.x + self.width * 0.1, self.y + self.width * 0.1))
            y_text_rect = self.y_text.get_rect(topright=(self.x - self.width * 0.1, self.y + self.width * 0.1))

            win.blit(self.x_text, x_text_rect)
            win.blit(self.y_text, y_text_rect)


    def get_hexagon_points(self):
        gap = self.width
        hex_radius = gap / (2 * math.cos(math.pi / 6))
        vert_dist = hex_radius * 1.5
        x_offset = (self.col * gap) + ((self.row % 2) * gap / 2)
        y_offset = (self.row * vert_dist)
        hex_points = []

        for i in range(6):
            angle_deg = 60 * i - 30
            angle_rad = math.pi / 180 * angle_deg
            hex_points.append((x_offset + hex_radius * math.cos(angle_rad),
                               y_offset + hex_radius * math.sin(angle_rad)))
        return hex_points


    def get_triangle_points(self):
        gap = self.width
        x_offset = self.col * gap
        y_offset = self.row * gap

        if (self.row + self.col) % 2 == 0:
            triangle_points = [(x_offset, y_offset + gap),
                               (x_offset + gap, y_offset + gap),
                               (x_offset + gap // 2, y_offset)]
        else:
            triangle_points = [(x_offset, y_offset),
                               (x_offset + gap, y_offset),
                               (x_offset + gap // 2, y_offset + gap)]

        return triangle_points

    def draw_arrow(self, win):
        if SHOW_ARROWS == True and self.predecessor and self.arrow_color:
            dx = (self.predecessor.x - self.x) * 0.6
            dy = (self.predecessor.y - self.y) * 0.6
            start_pos = (self.x + self.width // 2, self.y + self.width // 2)
            end_pos = (self.predecessor.x - dx + self.width // 2, self.predecessor.y - dy + self.width // 2)

            pygame.draw.line(win, self.arrow_color, start_pos, end_pos, 2)

            # Draw arrowhead
            angle = math.atan2(dy, dx)
            arrow_length = 10
            arrow_angle1 = angle + math.pi / 6
            arrow_angle2 = angle - math.pi / 6

            arrow_x1 = end_pos[0] - arrow_length * math.cos(arrow_angle1)
            arrow_y1 = end_pos[1] - arrow_length * math.sin(arrow_angle1)
            arrow_x2 = end_pos[0] - arrow_length * math.cos(arrow_angle2)
            arrow_y2 = end_pos[1] - arrow_length * math.sin(arrow_angle2)

            pygame.draw.line(win, self.arrow_color, end_pos, (arrow_x1, arrow_y1), 2)
            pygame.draw.line(win, self.arrow_color, end_pos, (arrow_x2, arrow_y2), 2)

    def update_arrow(self):
        if self.predecessor and not self.is_barrier() and not self.is_start() and not self.is_end():
            self.arrow_color = GREY
        else:
            self.arrow_color = None

    def update_neighbors(self, grid):

        if mode == "square":
            self.neighbors = []
            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
                self.neighbors.append(grid[self.row + 1][self.col])

            if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
                self.neighbors.append(grid[self.row - 1][self.col])

            if self.col < len(grid[self.row]) - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
                self.neighbors.append(grid[self.row][self.col + 1])

            if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
                self.neighbors.append(grid[self.row][self.col - 1])

            if DIAGONAL:
                if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_barrier():  # UP-LEFT
                    self.neighbors.append(grid[self.row - 1][self.col - 1])

                if self.row > 0 and self.col < self.total_rows - 1 and not grid[self.row - 1][
                    self.col + 1].is_barrier():  # UP-RIGHT
                    self.neighbors.append(grid[self.row - 1][self.col + 1])

                if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][
                    self.col - 1].is_barrier():  # DOWN-LEFT
                    self.neighbors.append(grid[self.row + 1][self.col - 1])

                if self.row < self.total_rows - 1 and self.col < self.total_rows - 1 and not grid[self.row + 1][
                    self.col + 1].is_barrier():  # DOWN-RIGHT
                    self.neighbors.append(grid[self.row + 1][self.col + 1])

        elif mode == "hexagon" or mode == "triangle":
            self.neighbors = []
            directions_odd = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (1, 1)]
            directions_even = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]

            directions = directions_even if self.col % 2 == 0 else directions_odd

            for dr, dc in directions:
                new_row, new_col = self.row + dr, self.col + dc
                if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
                    neighbor = grid[new_row][new_col]
                    if not neighbor.is_barrier():
                        if dr == 0 or dc == 0:
                            self.neighbors.append(neighbor)
                        else:
                            first_barrier = grid[self.row][self.col + dc]
                            second_barrier = grid[self.row + dr][self.col]
                            if not first_barrier.is_barrier() and not second_barrier.is_barrier():
                                self.neighbors.append(neighbor)

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, start):
    path = []
    while current in came_from:
        next_node = came_from[current]
        path.append(current)
        if current != start:
            current.make_path()
            current.predecessor = next_node
            current.arrow_color = BLACK  # Add this line
        current = next_node
    return len(path)


def make_grid(rows, width):
    grid = []
    gap = width // rows
    hex_radius = gap / (2 * math.cos(math.pi / 6))
    vert_dist = hex_radius * 1.5
    total_rows = int((width // vert_dist) - 1)

    if mode == "square":
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)
    elif mode == "hexagon":
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)
    elif mode == "triangle":
        for i in range(total_rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, total_rows)
                grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    hex_radius = gap / (2 * math.cos(math.pi / 6))
    vert_dist = hex_radius * 1.5

    if mode == "square":
        for i in range(rows):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
        pygame.draw.line(win, GREY, (0, width - 1), (width, width - 1))  # Bottom line
        pygame.draw.line(win, GREY, (width - 1, 0), (width - 1, width))  # Right line
    elif mode == "hexagon":
        for i in range(rows):
            for j in range(rows):
                x_offset = (j * gap) + ((i % 2) * gap / 2)
                y_offset = (i * vert_dist)
                if 0 <= x_offset < width and 0 <= y_offset < width:
                    hex_points = []
                    for k in range(6):
                        angle_deg = 60 * k - 30
                        angle_rad = math.pi / 180 * angle_deg
                        hex_points.append((x_offset + hex_radius * math.cos(angle_rad),
                                           y_offset + hex_radius * math.sin(angle_rad)))
                    pygame.draw.polygon(win, GREY, hex_points, 1)
    elif mode == "triangle":
        for i in range(rows):
            for j in range(rows):
                x_offset = j * gap
                y_offset = i * gap

                if (i + j) % 2 == 0:
                    triangle_points = [(x_offset, y_offset + gap),
                                       (x_offset + gap, y_offset + gap),
                                       (x_offset + gap // 2, y_offset)]
                else:
                    triangle_points = [(x_offset, y_offset),
                                       (x_offset + gap, y_offset),
                                       (x_offset + gap // 2, y_offset + gap)]

                pygame.draw.polygon(win, GREY, triangle_points, 1)

def draw(win, grid, rows, width, time_elapsed, algorithm_completed, SURFACE):

    if SURFACE == GRID_SURFACE:
        GRID_SURFACE.fill(DARK_BG)
        for row in grid:
            for spot in row:
                spot.draw(GRID_SURFACE, time_elapsed, algorithm_completed)
                spot.draw_arrow(GRID_SURFACE)
        draw_grid(GRID_SURFACE, rows, width)
        # draw surface
        win.blit(GRID_SURFACE, (frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2, top_bar.rect.height + 5))


    elif SURFACE == GRID_SURFACE2_1:
        GRID_SURFACE2_1.fill(DARK_BG)
        for row in grid:
            for spot2_1 in row:
                spot2_1.draw(GRID_SURFACE2_1, time_elapsed, algorithm_completed)
                spot2_1.draw_arrow(GRID_SURFACE2_1)
        draw_grid(GRID_SURFACE2_1, rows, width)
        # draw surface
        win.blit(GRID_SURFACE2_1, (frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2 - 100, top_bar.rect.height + 200))
    elif SURFACE == GRID_SURFACE2_2:
        GRID_SURFACE2_2.fill(DARK_BG)
        for row in grid:
            for spot2_2 in row:
                spot2_2.draw(GRID_SURFACE2_2, time_elapsed, algorithm_completed)
                spot2_2.draw_arrow(GRID_SURFACE2_2)
        draw_grid(GRID_SURFACE2_2, rows, width)
        # draw surface
        win.blit(GRID_SURFACE2_2, ((frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2) + 500, top_bar.rect.height + 200))


    elif SURFACE == GRID_SURFACE3_1:
        GRID_SURFACE3_1.fill(DARK_BG)
        for row in grid:
            for spot3_1 in row:
                spot3_1.draw(GRID_SURFACE3_1, time_elapsed, algorithm_completed)
                spot3_1.draw_arrow(GRID_SURFACE3_1)
        draw_grid(GRID_SURFACE3_1, rows, width)
        # draw surface
        win.blit(GRID_SURFACE3_1, (frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2 , top_bar.rect.height + 30))
    elif SURFACE == GRID_SURFACE3_2:
        GRID_SURFACE3_2.fill(DARK_BG)
        for row in grid:
            for spot3_2 in row:
                spot3_2.draw(GRID_SURFACE3_2, time_elapsed, algorithm_completed)
                spot3_2.draw_arrow(GRID_SURFACE2_2)
        draw_grid(GRID_SURFACE3_2, rows, width)
        # draw surface
        win.blit(GRID_SURFACE3_2, ((frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2) + 500, top_bar.rect.height + 30))

    elif SURFACE == GRID_SURFACE3_3:
        GRID_SURFACE3_3.fill(DARK_BG)
        for row in grid:
            for spot3_3 in row:
                spot3_3.draw(GRID_SURFACE3_3, time_elapsed, algorithm_completed)
                spot3_3.draw_arrow(GRID_SURFACE3_3)
        draw_grid(GRID_SURFACE3_3, rows, width)
        # draw surface
        win.blit(GRID_SURFACE3_3, ((frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 4.5), top_bar.rect.height + 475))



    elif SURFACE == GRID_SURFACE4_1:
        GRID_SURFACE4_1.fill(DARK_BG)
        for row in grid:
            for spot4_1 in row:
                spot4_1.draw(GRID_SURFACE4_1, time_elapsed, algorithm_completed)
                spot4_1.draw_arrow(GRID_SURFACE4_1)
        draw_grid(GRID_SURFACE4_1, rows, width)
        # draw surface
        win.blit(GRID_SURFACE4_1, (frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2, top_bar.rect.height + 30))

    elif SURFACE == GRID_SURFACE4_2:
        GRID_SURFACE4_2.fill(DARK_BG)
        for row in grid:
            for spot4_2 in row:
                spot4_2.draw(GRID_SURFACE4_2, time_elapsed, algorithm_completed)
                spot4_2.draw_arrow(GRID_SURFACE2_2)
        draw_grid(GRID_SURFACE4_2, rows, width)
        # draw surface
        win.blit(GRID_SURFACE4_2,
                 ((frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2) + 500, top_bar.rect.height + 30))

    elif SURFACE == GRID_SURFACE4_3:
        GRID_SURFACE4_3.fill(DARK_BG)
        for row in grid:
            for spot4_3 in row:
                spot4_3.draw(GRID_SURFACE4_3, time_elapsed, algorithm_completed)
                spot4_3.draw_arrow(GRID_SURFACE4_3)
        draw_grid(GRID_SURFACE4_3, rows, width)
        # draw surface
        win.blit(GRID_SURFACE4_3,
                 ((frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2), top_bar.rect.height + 475))
    elif SURFACE == GRID_SURFACE4_4:
        GRID_SURFACE4_4.fill(DARK_BG)
        for row in grid:
            for spot4_4 in row:
                spot4_4.draw(GRID_SURFACE4_4, time_elapsed, algorithm_completed)
                spot4_4.draw_arrow(GRID_SURFACE4_4)
        draw_grid(GRID_SURFACE4_4, rows, width)
        # draw surface
        win.blit(GRID_SURFACE4_4,
                 ((frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2) + 500, top_bar.rect.height + 475))

    # THIS IS THE BUFFER PROBLEM!!!! FIX IT NEXT TIME BRO
    if algorithm_completed:
        pygame.display.update()


def get_clicked_pos(pos, rows, width, grid):
    if mode == "square":
        gap = width // rows
        y, x = pos

        row = y // gap
        col = x // gap

        return row, col

    elif mode == "hexagon":
        gap = width // rows
        hex_radius = gap / (2 * math.cos(math.pi / 6))
        vert_dist = hex_radius * 1.5
        x, y = pos

        approx_row = int(y // vert_dist)
        approx_col = int((x - (approx_row % 2) * gap / 2) // gap)

        min_distance = float("inf")
        min_row = None
        min_col = None

        for row in range(approx_row - 1, approx_row + 2):
            for col in range(approx_col - 1, approx_col + 2):
                if 0 <= row < rows and 0 <= col < rows:
                    hex_points = grid[row][col].get_hexagon_points()
                    hex_center = (sum(pt[0] for pt in hex_points) / 6, sum(pt[1] for pt in hex_points) / 6)
                    distance = (hex_center[0] - x) ** 2 + (hex_center[1] - y) ** 2
                    if distance < min_distance:
                        min_distance = distance
                        min_row = row
                        min_col = col

        return min_row, min_col

    elif mode == "triangle":
        gap = width // rows
        x, y = pos

        approx_row = int(y // gap)
        approx_col = int(x // gap)

        min_distance = float("inf")
        min_row = None
        min_col = None

        for row in range(approx_row - 1, approx_row + 2):
            for col in range(approx_col - 1, approx_col + 2):
                if 0 <= row < rows and 0 <= col < rows:
                    triangle_points = grid[row][col].get_triangle_points()
                    triangle_center = (sum(pt[0] for pt in triangle_points) / 3,
                                       sum(pt[1] for pt in triangle_points) / 3)
                    distance = (triangle_center[0] - x) ** 2 + (triangle_center[1] - y) ** 2
                    if distance < min_distance:
                        min_distance = distance
                        min_row = row
                        min_col = col

        return min_row, min_col


def reset_grid(grid, start, end):
    for row in grid:
        for spot in row:
            if spot != start and spot != end and not spot.is_barrier():
                spot.reset()
                spot.predecessor = None  # Add this line
                spot.arrow_color = None  # Add this line


def generate_obstacles(grid, start, end):
    for row in grid:
        for spot in row:
            if random.random() < 0.3 and spot != start and spot != end:
                spot.make_barrier()


# binary tree maze
def generate_maze(grid, start, end):
    # Create barriers on the grid
    for row in grid:
        for spot in row:
            if not spot.is_barrier():
                spot.make_barrier()

    # Create paths in the grid
    for x in range(1, len(grid) - 1, 2):
        for y in range(1, len(grid[0]) - 1, 2):
            grid[x][y].reset()
            if x == 1 and y > 1:
                grid[x][y - 1].reset()
            elif x > 1:
                if y == 1:
                    grid[x - 1][y].reset()
                else:
                    direction = random.choice(['UP', 'LEFT'])
                    if direction == 'UP':
                        grid[x][y - 1].reset()
                    elif direction == 'LEFT':
                        grid[x - 1][y].reset()

    start_x, start_y = start.get_pos()
    end_x, end_y = end.get_pos()

    grid[start_x][start_y] = start
    grid[end_x][end_y] = end
    start.make_start()
    end.make_end()



def update_mode(ROWS, width, loc_mode):
    global mode
    mode = loc_mode
    start, end = None, None
    grid = make_grid(ROWS, width)

def update_visuals(option):
    global SHOW_ARROWS
    global SHOW_COORDS
    if option == "Arrows":
        SHOW_ARROWS = not SHOW_ARROWS
    if option == "Coords":
        SHOW_COORDS = not SHOW_COORDS

def update_diagonal():
    global DIAGONAL
    DIAGONAL = not DIAGONAL


from functions import *


def change_bg():
    global BG_COLOR
    global DARK_MODE
    global WHITE, GREY
    global DARK_BG
    DARK_MODE = not DARK_MODE
    if DARK_MODE == False:
        DARK_BG = "#FFFFFF"
        bg_mode_button.set_text("Dark mode")
        WHITE = (255, 255, 255)
        GREY = (60, 63, 65)
        BG_COLOR = (219, 222, 227)
        image.set_image(image_surface_light)
        corner_icon.set_image(pygame.image.load('icon_light.png'))
        change_theme()
    else:
        DARK_BG = "#3C3F41"
        bg_mode_button.set_text("Light mode")
        GREY = (220, 220, 220)
        WHITE = (60, 63, 65)
        BG_COLOR = (0, 0, 0)
        image.set_image(image_surface)
        corner_icon.set_image(pygame.image.load('icon.png'))
        reset_theme()


def main(win, width):
    global chosen_heuristic, RECORDING
    global GRID1, GRID2, GRID3, GRID4

    total_nodes_expanded: list = []
    total_steps: list = []
    total_path_length: list = []
    total_time_taken: list = []

    results_window.hide()
    grids_window.hide()
    grid_nr_error_label.hide()
    algorithm_error_label.hide()
    colors_window.hide()

    algo_list = []


    ROWS = 10
    # 1 grid
    grid = make_grid(ROWS, GRID_WIDTH)
    # 2 grids
    grid2_1 = make_grid(ROWS, GRID_WIDTH2)
    grid2_2 = make_grid(ROWS, GRID_WIDTH2)

    # 3 grids
    grid3_1 = make_grid(ROWS, GRID_WIDTH3)
    grid3_2 = make_grid(ROWS, GRID_WIDTH3)
    grid3_3 = make_grid(ROWS, GRID_WIDTH3)

    # 4 grids
    grid4_1 = make_grid(ROWS, GRID_WIDTH4)
    grid4_2 = make_grid(ROWS, GRID_WIDTH4)
    grid4_3 = make_grid(ROWS, GRID_WIDTH4)
    grid4_4 = make_grid(ROWS, GRID_WIDTH4)

    algorithm_completed = False

    #1 grid
    start = None
    end = None

    # 2 grids
    start2_1 = None
    end2_1 = None

    start2_2 = None
    end2_2 = None

    # 3 grids
    start3_1 = None
    end3_1 = None
    start3_2 = None
    end3_2 = None
    start3_3 = None
    end3_3 = None

    # 4 grids
    start4_1 = None
    end4_1 = None
    start4_2 = None
    end4_2 = None
    start4_3 = None
    end4_3 = None
    start4_4 = None
    end4_4 = None


    dragging_start = False
    dragging_end = False

    # 1 grid
    prev_start_spot = None
    prev_end_spot = None

    # 2 grids
    prev_start_spot2_1 = None
    prev_end_spot2_1 = None

    prev_start_spot2_2 = None
    prev_end_spot2_2 = None

    # 3 grids
    prev_start_spot3_1 = None
    prev_end_spot3_1 = None
    prev_start_spot3_2 = None
    prev_end_spot3_2 = None
    prev_start_spot3_3 = None
    prev_end_spot3_3 = None

    # 4 grids
    prev_start_spot4_1 = None
    prev_end_spot4_1 = None
    prev_start_spot4_2 = None
    prev_end_spot4_2 = None
    prev_start_spot4_3 = None
    prev_end_spot4_3 = None
    prev_start_spot4_4 = None
    prev_end_spot4_4 = None

    pygame.freetype.init()

    clock = pygame.time.Clock()  # Add this line to create the clock object

    run = True
    while run:
        time_delta = clock.tick(60) / 1000.0
        clock.tick(60)  # Limit the frame rate to 60 FPS
        time_elapsed = pygame.time.get_ticks() / 1000  # Get the elapsed time in seconds
        if GRID1:
            width = GRID_WIDTH
        elif GRID2:
            width = GRID_WIDTH2
        elif GRID3:
            width = GRID_WIDTH3
        elif GRID4:
            width = GRID_WIDTH4

        for event in pygame.event.get():


            delay_time = delay_slider.get_current_value()
            if event.type == pygame.QUIT:
                run = False

            if GRID1:
                pos = pygame.mouse.get_pos()
                # Calculate the offset from the top-left corner of the frame_middle
                offset_x = frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2
                offset_y = top_bar.rect.height + 5

                # Subtract the offsets to get the correct position within the grid
                pos = (pos[0] - offset_x, pos[1] - offset_y)
                on_grid = 0 <= pos[0] < GRID_WIDTH and 0 <= pos[1] < GRID_WIDTH

                if on_grid:
                    row, col = get_clicked_pos(pos, ROWS, width, grid)
                    if row is None or col is None:  # Skip if None is returned
                        continue
                    spot = grid[row][col]
            if GRID2:
                pos = pygame.mouse.get_pos()
                # Calculate the offset from the top-left corner of the frame_middle
                offset_x = frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2 - 100
                offset_y = top_bar.rect.height + 200

                # Subtract the offsets to get the correct position within the grid
                pos = (pos[0] - offset_x, pos[1] - offset_y)
                on_grid = 0 <= pos[0] < GRID_WIDTH2 and 0 <= pos[1] < GRID_WIDTH2

                if on_grid:
                    row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH2, grid)
                    if row is None or col is None:  # Skip if None is returned
                        continue
                    spot2_1 = grid2_1[row][col]
                    spot2_2 = grid2_2[row][col]

            if GRID3:
                pos = pygame.mouse.get_pos()
                # Calculate the offset from the top-left corner of the frame_middle
                offset_x = frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2
                offset_y = top_bar.rect.height + 30

                # Subtract the offsets to get the correct position within the grid
                pos = (pos[0] - offset_x, pos[1] - offset_y)
                on_grid = 0 <= pos[0] < GRID_WIDTH3 and 0 <= pos[1] < GRID_WIDTH3

                if on_grid:
                    row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH3, grid)
                    if row is None or col is None:  # Skip if None is returned
                        continue
                    spot3_1 = grid3_1[row][col]
                    spot3_2 = grid3_2[row][col]
                    spot3_3 = grid3_3[row][col]

            if GRID4:
                pos = pygame.mouse.get_pos()
                # Calculate the offset from the top-left corner of the frame_middle
                offset_x = frame_middle.rect.center[0] - GRID_SURFACE.get_width() // 2
                offset_y = top_bar.rect.height + 30

                # Subtract the offsets to get the correct position within the grid
                pos = (pos[0] - offset_x, pos[1] - offset_y)
                on_grid = 0 <= pos[0] < GRID_WIDTH4 and 0 <= pos[1] < GRID_WIDTH4

                if on_grid:
                    row, col = get_clicked_pos(pos, ROWS, GRID_WIDTH4, grid4_1)
                    if row is None or col is None:  # Skip if None is returned
                        continue
                    spot4_1 = grid4_1[row][col]
                    spot4_2 = grid4_2[row][col]
                    spot4_3 = grid4_3[row][col]
                    spot4_4 = grid4_4[row][col]


            if GRID1:
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
                            algorithm_completed = False
                            dragging_start = True

                        if spot == end:
                            algorithm_completed = False
                            dragging_end = True

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    if on_grid:
                        spot.reset()
                        spot.predecessor = None
                        spot.arrow_color = None

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
                    reset_grid(grid, start, end)

                if dragging_end and on_grid and spot != start and not spot.is_barrier():
                    if prev_end_spot:
                        prev_end_spot.reset()
                    prev_end_spot = spot
                    end.reset()
                    end = spot
                    end.make_end()
                    reset_grid(grid, start, end)

            if GRID2:
                if pygame.mouse.get_pressed()[0]:  # LEFT
                    if on_grid:
                        if not start2_1 and spot2_1 != end and not dragging_end and not spot2_1.is_barrier():
                            start2_1 = spot2_1
                            start2_1.make_start()
                            dragging_start = True

                            start2_2 = spot2_2
                            start2_2.make_start()

                        elif not end2_1 and spot2_1 != start2_1 and not dragging_start and not spot2_1.is_barrier():
                            end2_1 = spot2_1
                            end2_1.make_end()
                            dragging_end = True

                            end2_2 = spot2_2
                            end2_2.make_end()

                        elif spot2_1 != end2_1 and spot2_1 != start2_1 and not dragging_start and not dragging_end:
                            spot2_1.make_barrier()
                            spot2_2.make_barrier()

                        if spot2_1 == start2_1:
                            algorithm_completed = False
                            dragging_start = True

                        if spot2_1 == end2_1:
                            algorithm_completed = False
                            dragging_end = True

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    if on_grid:
                        spot2_1.reset()
                        spot2_2.reset()

                        if spot2_1 == start2_1:
                            start2_1 = None
                            start2_2 = None
                            dragging_start = False
                        elif spot2_1 == end2_1:
                            end2_1 = None
                            end2_2 = None
                            dragging_end = False

                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_start = False
                    dragging_end = False
                    prev_start_spot2_1 = None
                    prev_end_spot2_1 = None
                    prev_start_spot2_2 = None
                    prev_end_spot2_2 = None

                if dragging_start and on_grid and spot2_1 != end2_1 and not spot2_1.is_barrier():
                    if prev_start_spot2_1:
                        prev_start_spot2_1.reset()
                    prev_start_spot2_1 = spot2_1
                    start2_1.reset()
                    start2_1 = spot2_1
                    start2_1.make_start()
                    reset_grid(grid2_1, start2_1, end2_1)

                    if prev_start_spot2_2:
                        prev_start_spot2_2.reset()
                    prev_start_spot2_2 = spot2_2
                    start2_2.reset()
                    start2_2 = spot2_2
                    start2_2.make_start()
                    reset_grid(grid2_2, start2_2, end2_2)

                if dragging_end and on_grid and spot2_1 != start and not spot2_1.is_barrier():
                    if prev_end_spot2_1:
                        prev_end_spot2_1.reset()
                    prev_end_spot2_1 = spot2_1
                    end2_1.reset()
                    end2_1 = spot2_1
                    end2_1.make_end()
                    reset_grid(grid2_1, start2_1, end2_1)

                    if prev_end_spot2_2:
                        prev_end_spot2_2.reset()
                    prev_end_spot2_2 = spot2_2
                    end2_2.reset()
                    end2_2 = spot2_2
                    end2_2.make_end()
                    reset_grid(grid2_2, start2_2, end2_2)

            if GRID3:
                if pygame.mouse.get_pressed()[0]:  # LEFT
                    if on_grid:
                        if not start3_1 and spot3_1 != end and not dragging_end and not spot3_1.is_barrier():
                            start3_1 = spot3_1
                            start3_1.make_start()
                            dragging_start = True

                            start3_2 = spot3_2
                            start3_2.make_start()
                            start3_3 = spot3_3
                            start3_3.make_start()

                        elif not end3_1 and spot3_1 != start3_1 and not dragging_start and not spot3_1.is_barrier():
                            end3_1 = spot3_1
                            end3_1.make_end()
                            dragging_end = True

                            end3_2 = spot3_2
                            end3_2.make_end()
                            end3_3 = spot3_3
                            end3_3.make_end()

                        elif spot3_1 != end3_1 and spot3_1 != start3_1 and not dragging_start and not dragging_end:
                            spot3_1.make_barrier()
                            spot3_2.make_barrier()
                            spot3_3.make_barrier()

                        if spot3_1 == start3_1:
                            algorithm_completed = False
                            dragging_start = True

                        if spot3_1 == end3_1:
                            algorithm_completed = False
                            dragging_end = True

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    if on_grid:
                        spot3_1.reset()
                        spot3_2.reset()
                        spot3_3.reset()

                        if spot3_1 == start3_1:
                            start3_1 = None
                            start3_2 = None
                            start3_3 = None
                            dragging_start = False
                        elif spot3_1 == end3_1:
                            end3_1 = None
                            end3_2 = None
                            end3_3 = None
                            dragging_end = False

                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_start = False
                    dragging_end = False
                    prev_start_spot3_1 = None
                    prev_end_spot3_1 = None
                    prev_start_spot3_2 = None
                    prev_end_spot3_2 = None
                    prev_start_spot3_3 = None
                    prev_end_spot3_3 = None

                if dragging_start and on_grid and spot3_1 != end3_1 and not spot3_1.is_barrier():
                    if prev_start_spot3_1:
                        prev_start_spot3_1.reset()
                    prev_start_spot3_1 = spot3_1
                    start3_1.reset()
                    start3_1 = spot3_1
                    start3_1.make_start()
                    reset_grid(grid3_1, start3_1, end3_1)

                    if prev_start_spot3_2:
                        prev_start_spot3_2.reset()
                    prev_start_spot3_2 = spot3_2
                    start3_2.reset()
                    start3_2 = spot3_2
                    start3_2.make_start()
                    reset_grid(grid3_2, start3_2, end3_2)

                    if prev_start_spot3_3:
                        prev_start_spot3_3.reset()
                    prev_start_spot3_3 = spot3_3
                    start3_3.reset()
                    start3_3 = spot3_3
                    start3_3.make_start()
                    reset_grid(grid3_3, start3_3, end3_3)

                if dragging_end and on_grid and spot3_1 != start and not spot3_1.is_barrier():
                    if prev_end_spot3_1:
                        prev_end_spot3_1.reset()
                    prev_end_spot3_1 = spot3_1
                    end3_1.reset()
                    end3_1 = spot3_1
                    end3_1.make_end()
                    reset_grid(grid3_1, start3_1, end3_1)

                    if prev_end_spot3_2:
                        prev_end_spot3_2.reset()
                    prev_end_spot3_2 = spot3_2
                    end3_2.reset()
                    end3_2 = spot3_2
                    end3_2.make_end()
                    reset_grid(grid3_2, start3_2, end3_2)

                    if prev_end_spot3_3:
                        prev_end_spot3_3.reset()
                    prev_end_spot3_3 = spot3_3
                    end3_3.reset()
                    end3_3 = spot3_3
                    end3_3.make_end()
                    reset_grid(grid3_3, start3_3, end3_3)

            if GRID4:
                if pygame.mouse.get_pressed()[0]:  # LEFT
                    if on_grid:
                        if not start4_1 and spot4_1 != end and not dragging_end and not spot4_1.is_barrier():
                            start4_1 = spot4_1
                            start4_1.make_start()
                            dragging_start = True

                            start4_2 = spot4_2
                            start4_2.make_start()
                            start4_3 = spot4_3
                            start4_3.make_start()
                            start4_4 = spot4_4
                            start4_4.make_start()

                        elif not end4_1 and spot4_1 != start4_1 and not dragging_start and not spot4_1.is_barrier():
                            end4_1 = spot4_1
                            end4_1.make_end()
                            dragging_end = True

                            end4_2 = spot4_2
                            end4_2.make_end()
                            end4_3 = spot4_3
                            end4_3.make_end()
                            end4_4 = spot4_4
                            end4_4.make_end()

                        elif spot4_1 != end4_1 and spot4_1 != start4_1 and not dragging_start and not dragging_end:
                            spot4_1.make_barrier()
                            spot4_2.make_barrier()
                            spot4_3.make_barrier()
                            spot4_4.make_barrier()

                        if spot4_1 == start4_1:
                            algorithm_completed = False
                            dragging_start = True

                        if spot4_1 == end4_1:
                            algorithm_completed = False
                            dragging_end = True

                elif pygame.mouse.get_pressed()[2]:  # RIGHT
                    if on_grid:
                        spot4_1.reset()
                        spot4_2.reset()
                        spot4_3.reset()
                        spot4_4.reset()

                        if spot4_1 == start4_1:
                            start4_1 = None
                            start4_2 = None
                            start4_3 = None
                            start4_4 = None
                            dragging_start = False
                        elif spot4_1 == end4_1:
                            end4_1 = None
                            end4_2 = None
                            end4_3 = None
                            end4_4 = None
                            dragging_end = False

                if event.type == pygame.MOUSEBUTTONUP:
                    dragging_start = False
                    dragging_end = False
                    prev_start_spot4_1 = None
                    prev_end_spot4_1 = None
                    prev_start_spot4_2 = None
                    prev_end_spot4_2 = None
                    prev_start_spot4_3 = None
                    prev_end_spot4_3 = None
                    prev_start_spot4_4 = None
                    prev_end_spot4_4 = None

                if dragging_start and on_grid and spot4_1 != end4_1 and not spot4_1.is_barrier():
                    if prev_start_spot4_1:
                        prev_start_spot4_1.reset()
                    prev_start_spot4_1 = spot4_1
                    start4_1.reset()
                    start4_1 = spot4_1
                    start4_1.make_start()
                    reset_grid(grid4_1, start4_1, end4_1)

                    if prev_start_spot4_2:
                        prev_start_spot4_2.reset()
                    prev_start_spot4_2 = spot4_2
                    start4_2.reset()
                    start4_2 = spot4_2
                    start4_2.make_start()
                    reset_grid(grid4_2, start4_2, end4_2)

                    if prev_start_spot4_3:
                        prev_start_spot4_3.reset()
                    prev_start_spot4_3 = spot4_3
                    start4_3.reset()
                    start4_3 = spot4_3
                    start4_3.make_start()
                    reset_grid(grid4_3, start4_3, end4_3)

                    if prev_start_spot4_4:
                        prev_start_spot4_4.reset()
                    prev_start_spot4_4 = spot4_4
                    start4_4.reset()
                    start4_4 = spot4_4
                    start4_4.make_start()
                    reset_grid(grid4_4, start4_4, end4_4)

                if dragging_end and on_grid and spot4_1 != start and not spot4_1.is_barrier():
                    if prev_end_spot4_1:
                        prev_end_spot4_1.reset()
                    prev_end_spot4_1 = spot4_1
                    end4_1.reset()
                    end4_1 = spot4_1
                    end4_1.make_end()
                    reset_grid(grid4_1, start4_1, end4_1)

                    if prev_end_spot4_2:
                        prev_end_spot4_2.reset()
                    prev_end_spot4_2 = spot4_2
                    end4_2.reset()
                    end4_2 = spot4_2
                    end4_2.make_end()
                    reset_grid(grid4_2, start4_2, end4_2)

                    if prev_end_spot4_3:
                        prev_end_spot4_3.reset()
                    prev_end_spot4_3 = spot4_3
                    end4_3.reset()
                    end4_3 = spot4_3
                    end4_3.make_end()
                    reset_grid(grid4_3, start4_3, end4_3)

                    if prev_end_spot4_4:
                        prev_end_spot4_4.reset()
                    prev_end_spot4_4 = spot4_4
                    end4_4.reset()
                    end4_4 = spot4_4
                    end4_4.make_end()
                    reset_grid(grid4_4, start4_4, end4_4)


            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    reset_grid(grid, start, end)  # Reset the grid before running the algorithm
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    chosen_heuristic = algorithms.heuristic(algorithms.Heuristic.EUCLIDEAN)
                    algorithm_completed = algorithms.best_first_search(
                        lambda: draw(win, grid, ROWS, width, time_elapsed, algorithm_completed), grid, start, end,
                        chosen_heuristic, delay_time)

            if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_element == drop_down:
                    if drop_down.selected_option == "A*":
                        heuristic_options.enable()
                        algo_info.set_text(astar_text)
                    elif drop_down.selected_option == "Dijkstra":
                        heuristic_options.disable()
                        algo_info.set_text(dijkstra_text)
                    elif drop_down.selected_option == "Greedy Best-First-Search":
                        heuristic_options.enable()
                        algo_info.set_text(greedy_text)
                    elif drop_down.selected_option == "Breadth-First-Search":
                        heuristic_options.disable()
                        algo_info.set_text(bfs_text)
                    elif drop_down.selected_option == "Depth-First-Search":
                        heuristic_options.disable()
                        algo_info.set_text(dfs_text)



            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == grid_size_slider:
                    if grid_size_slider.value_range == (0, len(grid_sizes2) - 1):
                        grid_size_label.set_text(str(grid_sizes2[int(grid_size_slider.get_current_value())]))
                        new_rows = grid_sizes2[int(grid_size_slider.get_current_value())]
                    elif grid_size_slider.value_range == (0, len(grid_sizes3) - 1):
                        grid_size_label.set_text(str(grid_sizes3[int(grid_size_slider.get_current_value())]))
                        new_rows = grid_sizes3[int(grid_size_slider.get_current_value())]
                    else:
                        grid_size_label.set_text(str(grid_sizes[int(grid_size_slider.get_current_value())]))
                        new_rows = grid_sizes[int(grid_size_slider.get_current_value())]
                    if new_rows != ROWS:
                        ROWS = new_rows
                        if GRID1:
                            grid = make_grid(ROWS, width)
                            start = None
                            end = None
                        if GRID2:
                            grid2_1 = make_grid(ROWS, width)
                            grid2_2 = make_grid(ROWS, width)
                            start2_1 = None
                            end2_1 = None
                            start2_2 = None
                            end2_2 = None
                        if GRID3:
                            grid3_1 = make_grid(ROWS, width)
                            grid3_2 = make_grid(ROWS, width)
                            grid3_3 = make_grid(ROWS, width)
                            start3_1 = None
                            end3_1 = None
                            start3_2 = None
                            end3_2 = None
                            start3_3 = None
                            end3_3 = None
                        if GRID4:
                            grid4_1 = make_grid(ROWS, width)
                            grid4_2 = make_grid(ROWS, width)
                            grid4_3 = make_grid(ROWS, width)
                            grid4_4 = make_grid(ROWS, width)
                            start4_1 = None
                            end4_1 = None
                            start4_2 = None
                            end4_2 = None
                            start4_3 = None
                            end4_3 = None
                            start4_4 = None
                            end4_4 = None
                        algorithm_completed = False

                if event.ui_element == delay_slider:
                    delay_label.set_text(str(delay_slider.get_current_value()) + " ms")

                if event.ui_element == grid_nr_slider:
                    grid_nr_label.set_text(str(grid_nr_slider.get_current_value()))


            if event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == heuristic_options:
                    if heuristic_options.get_single_selection() == "Manhattan":
                        chosen_heuristic = algorithms.heuristic(algorithms.Heuristic.MANHATTAN)
                    elif heuristic_options.get_single_selection() == "Euclidean":
                        chosen_heuristic = algorithms.heuristic(algorithms.Heuristic.EUCLIDEAN)
                    elif heuristic_options.get_single_selection() == "Octile":
                        chosen_heuristic = algorithms.heuristic(algorithms.Heuristic.OCTILE)
                    elif heuristic_options.get_single_selection() == "Chebyshev":
                        chosen_heuristic = algorithms.heuristic(algorithms.Heuristic.CHEBYSHEV)

                if event.ui_element == spots_options:
                    global SHOW_ARROWS
                    global SHOW_COORDS
                    if spots_options.get_single_selection() == "translation.spots_square":
                        update_mode(ROWS, width, "square")
                    elif spots_options.get_single_selection() == "translation.spots_triangle":
                        SHOW_ARROWS = False
                        SHOW_COORDS = False
                        update_mode(ROWS, width, "triangle")
                    elif spots_options.get_single_selection() == "translation.spots_hexagon":
                        SHOW_ARROWS = False
                        SHOW_COORDS = False
                        update_mode(ROWS, width, "hexagon")

                if event.ui_element == arrow_coord_options:
                    if event.text == "translation.show_arrows":
                        update_visuals("Arrows")
                    if event.text == "translation.show_coords":
                        update_visuals("Coords")

                if event.ui_element == diagonal_option:
                    update_diagonal()

                if event.ui_element == grid_algorithms_option:
                    if len(grid_algorithms_option.get_multi_selection()) > grid_nr_slider.get_current_value():
                        grid_algorithms_option.remove_items(event.text)
                        grid_algorithms_option.add_items([event.text])
                        grid_nr_error_label.show()

            if event.type == pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION:
                if event.ui_element == arrow_coord_options:
                    if event.text == "translation.show_arrows":
                        update_visuals("Arrows")
                    if event.text == "translation.show_coords":
                        update_visuals("Coords")

                if event.ui_element == diagonal_option:
                    update_diagonal()


            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == exit_button:
                    run = False

                if event.ui_element == generate_grids_button:
                    nr = grid_nr_slider.get_current_value()
                    algo_list = grid_algorithms_option.get_multi_selection()
                    grid2_algo1_label.set_text("")
                    grid2_algo1_label.set_text("")
                    if len(grid_algorithms_option.get_multi_selection()) == grid_nr_slider.get_current_value():
                        grid_nr_error_label.hide()
                        ROWS = 10
                        if nr == 2:
                            grid_size_slider.value_range = (0, len(grid_sizes2) - 1)
                            grid_size_slider.set_current_value(1)
                        elif nr == 3 or nr == 4:
                            grid_size_slider.value_range = (0, len(grid_sizes3) - 1)
                            grid_size_slider.set_current_value(2)
                        if grid_size_slider.value_range == (0, len(grid_sizes2) - 1):
                            grid_size_label.set_text(str(grid_sizes2[int(grid_size_slider.get_current_value())]))
                        elif grid_size_slider.value_range == (0, len(grid_sizes3) - 1):
                            grid_size_label.set_text(str(grid_sizes3[int(grid_size_slider.get_current_value())]))
                        else:
                            grid_size_label.set_text(str(grid_sizes[int(grid_size_slider.get_current_value())]))
                        GRID1 = False
                        GRID2 = False
                        GRID3 = False
                        GRID4 = False
                        grid = make_grid(ROWS, width)
                        start = None
                        end = None

                        if nr == 2:
                            GRID2 = True
                            grid2_algo1_label.set_text(algo_list[0])
                            grid2_algo2_label.set_text(algo_list[1])
                        elif nr == 3:
                            GRID3 = True
                            grid3_algo1_label.set_text(algo_list[0])
                            grid3_algo2_label.set_text(algo_list[1])
                            grid3_algo3_label.set_text(algo_list[2])
                        elif nr == 4:
                            GRID4 = True
                            grid4_algo1_label.set_text(algo_list[0])
                            grid4_algo2_label.set_text(algo_list[1])
                            grid4_algo3_label.set_text(algo_list[2])
                            grid4_algo4_label.set_text(algo_list[3])

                        algorithm_completed = False
                        grids_window.hide()

                if event.ui_element == maze_button:
                    if start and end or start2_1 and end2_1 or start3_1 and end3_1 or start4_1 and end4_1:
                        if GRID1:
                            reset_grid(grid, start, end)
                            generate_maze(grid, start, end)
                        if GRID2:
                            reset_grid(grid2_1, start2_1, end2_1)
                            reset_grid(grid2_2, start2_2, end2_2)
                            seed = random.randint(0, 1000000)
                            random.seed(seed)
                            generate_maze(grid2_1, start2_1, end2_1)
                            random.seed(seed)
                            generate_maze(grid2_2, start2_2, end2_2)
                        if GRID3:
                            reset_grid(grid3_1, start3_1, end3_1)
                            reset_grid(grid3_2, start3_2, end3_2)
                            reset_grid(grid3_3, start3_3, end3_3)
                            seed = random.randint(0, 1000000)
                            random.seed(seed)
                            generate_maze(grid3_1, start3_1, end3_1)
                            random.seed(seed)
                            generate_maze(grid3_2, start3_2, end3_2)
                            random.seed(seed)
                            generate_maze(grid3_3, start3_3, end3_3)
                        if GRID4:
                            reset_grid(grid4_1, start4_1, end4_1)
                            reset_grid(grid4_2, start4_2, end4_2)
                            reset_grid(grid4_3, start4_3, end4_3)
                            reset_grid(grid4_4, start4_4, end4_4)
                            seed = random.randint(0, 1000000)
                            random.seed(seed)
                            generate_maze(grid4_1, start4_1, end4_1)
                            random.seed(seed)
                            generate_maze(grid4_2, start4_2, end4_2)
                            random.seed(seed)
                            generate_maze(grid4_3, start4_3, end4_3)
                            random.seed(seed)
                            generate_maze(grid4_4, start4_4, end4_4)


                if event.ui_element == obstacles_button:
                    if GRID1:
                        reset_grid(grid, start, end)
                        generate_obstacles(grid, start, end)
                    if GRID2:
                        reset_grid(grid2_1, start2_1, end2_1)
                        reset_grid(grid2_2, start2_2, end2_2)
                        seed = random.randint(0, 1000000)
                        random.seed(seed)
                        generate_obstacles(grid2_1, start2_1, end2_1)
                        random.seed(seed)
                        generate_obstacles(grid2_2, start2_2, end2_2)
                    if GRID3:
                        reset_grid(grid3_1, start3_1, end3_1)
                        reset_grid(grid3_2, start3_2, end3_2)
                        reset_grid(grid3_3, start3_3, end3_3)
                        seed = random.randint(0, 1000000)
                        random.seed(seed)
                        generate_obstacles(grid3_1, start3_1, end3_1)
                        random.seed(seed)
                        generate_obstacles(grid3_2, start3_2, end3_2)
                        random.seed(seed)
                        generate_obstacles(grid3_3, start3_3, end3_3)
                    if GRID4:
                        reset_grid(grid4_1, start4_1, end4_1)
                        reset_grid(grid4_2, start4_2, end4_2)
                        reset_grid(grid4_3, start4_3, end4_3)
                        reset_grid(grid4_4, start4_4, end4_4)
                        seed = random.randint(0, 1000000)
                        random.seed(seed)
                        generate_obstacles(grid4_1, start4_1, end4_1)
                        random.seed(seed)
                        generate_obstacles(grid4_2, start4_2, end4_2)
                        random.seed(seed)
                        generate_obstacles(grid4_3, start4_3, end4_3)
                        random.seed(seed)
                        generate_obstacles(grid4_4, start4_4, end4_4)


                if event.ui_element == clear_button:
                    if GRID1:
                        start = None
                        end = None
                        grid = make_grid(ROWS, width)
                    if GRID2:
                        start2_1 = None
                        end2_1 = None
                        grid2_1 = make_grid(ROWS, width)
                        start2_2 = None
                        end2_2 = None
                        grid2_2 = make_grid(ROWS, width)
                    if GRID3:
                        start3_1 = None
                        end3_1 = None
                        grid3_1 = make_grid(ROWS, width)
                        start3_2 = None
                        end3_2 = None
                        grid3_2 = make_grid(ROWS, width)
                        start3_3 = None
                        end3_3 = None
                        grid3_3 = make_grid(ROWS, width)
                    if GRID4:
                        start4_1 = None
                        end4_1 = None
                        grid4_1 = make_grid(ROWS, width)
                        start4_2 = None
                        end4_2 = None
                        grid4_2 = make_grid(ROWS, width)
                        start4_3 = None
                        end4_3 = None
                        grid4_3 = make_grid(ROWS, width)
                        start4_4 = None
                        end4_4 = None
                        grid4_4 = make_grid(ROWS, width)

                    nodes_entry.set_text("0")
                    steps_entry.set_text("0")
                    length_entry.set_text("0")
                    time_entry.set_text("0")

                if event.ui_element == run_algorithm:
                    if start and end or start2_1 and end2_1 or start3_1 and end3_1 or start4_1 and end4_1:
                        algorithm_error_label.hide()

                        if GRID1 == False:
                            algorithm_completed = True
                            total_nodes_expanded.clear()
                            total_steps.clear()
                            total_path_length.clear()
                            total_time_taken.clear()
                            for item in algo_list:
                                print(algo_list.index(item))
                                loc_grid, loc_start, loc_end, loc_surface = None, None, None, None
                                if GRID2 == True:
                                    if algo_list.index(item) == 0:
                                        loc_grid = grid2_1
                                        loc_start = start2_1
                                        loc_end = end2_1
                                        loc_surface = GRID_SURFACE2_1
                                    elif algo_list.index(item) == 1:
                                        loc_grid = grid2_2
                                        loc_start = start2_2
                                        loc_end = end2_2
                                        loc_surface = GRID_SURFACE2_2
                                if GRID3 == True:
                                    if algo_list.index(item) == 0:
                                        loc_grid = grid3_1
                                        loc_start = start3_1
                                        loc_end = end3_1
                                        loc_surface = GRID_SURFACE3_1
                                    elif algo_list.index(item) == 1:
                                        loc_grid = grid3_2
                                        loc_start = start3_2
                                        loc_end = end3_2
                                        loc_surface = GRID_SURFACE3_2
                                    elif algo_list.index(item) == 2:
                                        loc_grid = grid3_3
                                        loc_start = start3_3
                                        loc_end = end3_3
                                        loc_surface = GRID_SURFACE3_3
                                if GRID4 == True:
                                    if algo_list.index(item) == 0:
                                        loc_grid = grid4_1
                                        loc_start = start4_1
                                        loc_end = end4_1
                                        loc_surface = GRID_SURFACE4_1
                                    elif algo_list.index(item) == 1:
                                        loc_grid = grid4_2
                                        loc_start = start4_2
                                        loc_end = end4_2
                                        loc_surface = GRID_SURFACE4_2
                                    elif algo_list.index(item) == 2:
                                        loc_grid = grid4_3
                                        loc_start = start4_3
                                        loc_end = end4_3
                                        loc_surface = GRID_SURFACE4_3
                                    elif algo_list.index(item) == 3:
                                        loc_grid = grid4_4
                                        loc_start = start4_4
                                        loc_end = end4_4
                                        loc_surface = GRID_SURFACE4_4
                                if item == "A*":
                                    reset_grid(loc_grid, loc_start, loc_end)
                                    for row in loc_grid:
                                        for spot in row:
                                            spot.update_neighbors(loc_grid)
                                    algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.astar(
                                        lambda: draw(win, loc_grid, ROWS, width, time_elapsed, algorithm_completed,
                                                     loc_surface),
                                        loc_grid, loc_start, loc_end,
                                        chosen_heuristic, delay_time)
                                    total_nodes_expanded.append(expanded_nodes)
                                    total_steps.append(steps)
                                    total_path_length.append(path_length)
                                    total_time_taken.append(elapsed_time)
                                elif item == "Dijkstra":
                                    reset_grid(loc_grid, loc_start, loc_end)
                                    for row in loc_grid:
                                        for spot in row:
                                            spot.update_neighbors(loc_grid)
                                    algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.dijkstra(
                                        lambda: draw(win, loc_grid, ROWS, width, time_elapsed, algorithm_completed,
                                                     loc_surface),
                                        loc_grid, loc_start, loc_end,
                                        chosen_heuristic, delay_time)
                                    total_nodes_expanded.append(expanded_nodes)
                                    total_steps.append(steps)
                                    total_path_length.append(path_length)
                                    total_time_taken.append(elapsed_time)
                                elif item == "BFS":
                                    reset_grid(loc_grid, loc_start, loc_end)
                                    for row in loc_grid:
                                        for spot in row:
                                            spot.update_neighbors(loc_grid)
                                    algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.breadth_first_search(
                                        lambda: draw(win, loc_grid, ROWS, width, time_elapsed, algorithm_completed,
                                                     loc_surface),
                                        loc_grid, loc_start, loc_end,
                                        chosen_heuristic, delay_time)
                                    total_nodes_expanded.append(expanded_nodes)
                                    total_steps.append(steps)
                                    total_path_length.append(path_length)
                                    total_time_taken.append(elapsed_time)
                                elif item == "Greedy":
                                    reset_grid(loc_grid, loc_start, loc_end)
                                    for row in loc_grid:
                                        for spot in row:
                                            spot.update_neighbors(loc_grid)
                                    algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.best_first_search(
                                        lambda: draw(win, loc_grid, ROWS, width, time_elapsed, algorithm_completed,
                                                     loc_surface),
                                        loc_grid, loc_start, loc_end,
                                        chosen_heuristic, delay_time)
                                    total_nodes_expanded.append(expanded_nodes)
                                    total_steps.append(steps)
                                    total_path_length.append(path_length)
                                    total_time_taken.append(elapsed_time)
                                elif item == "DFS":
                                    reset_grid(loc_grid, loc_start, loc_end)
                                    for row in loc_grid:
                                        for spot in row:
                                            spot.update_neighbors(loc_grid)
                                    algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.depth_first_search(
                                        lambda: draw(win, loc_grid, ROWS, width, time_elapsed, algorithm_completed,
                                                     loc_surface),
                                        loc_grid, loc_start, loc_end,
                                        chosen_heuristic, delay_time)
                                    total_nodes_expanded.append(expanded_nodes)
                                    total_steps.append(steps)
                                    total_path_length.append(path_length)
                                    total_time_taken.append(elapsed_time)
                            create_plots(total_nodes_expanded, total_steps, total_path_length, total_time_taken, algo_list)
                            results_box.rebuild()
                            manager2.update(1)
                            results_window.show()

                        if drop_down.selected_option == "A*":
                            if GRID1:
                                algorithm_completed = True
                                reset_grid(grid, start, end)  # Reset the grid before running the algorithm
                                for row in grid:
                                    for spot in row:
                                        spot.update_neighbors(grid)
                                chosen_heuristic = algorithms.heuristic(algorithms.Heuristic.EUCLIDEAN)
                                algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.astar(
                                    lambda: draw(win, grid, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE), grid, start, end,
                                    chosen_heuristic, delay_time)
                                nodes_entry.set_text(str(expanded_nodes))
                                steps_entry.set_text(str(steps))
                                length_entry.set_text(str(path_length))
                                time_entry.set_text(f"{elapsed_time:.2f} s")


                        elif drop_down.selected_option == "Dijkstra":
                            if GRID1:
                                algorithm_completed = True
                                reset_grid(grid, start, end)  # Reset the grid before running the algorithm
                                for row in grid:
                                    for spot in row:
                                        spot.update_neighbors(grid)
                                algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.dijkstra(
                                    lambda: draw(win, grid, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE), grid, start, end,
                                    chosen_heuristic, delay_time)
                                nodes_entry.set_text(str(expanded_nodes))
                                steps_entry.set_text(str(steps))
                                length_entry.set_text(str(path_length))
                                time_entry.set_text(f"{elapsed_time:.2f} s")
                        elif drop_down.selected_option == "Greedy Best-First-Search":
                            if GRID1:
                                algorithm_completed = True
                                reset_grid(grid, start, end)  # Reset the grid before running the algorithm
                                for row in grid:
                                    for spot in row:
                                        spot.update_neighbors(grid)
                                algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.best_first_search(
                                    lambda: draw(win, grid, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE), grid, start, end,
                                    chosen_heuristic, delay_time)
                                nodes_entry.set_text(str(expanded_nodes))
                                steps_entry.set_text(str(steps))
                                length_entry.set_text(str(path_length))
                                time_entry.set_text(f"{elapsed_time:.2f} s")
                        elif drop_down.selected_option == "Breadth-First-Search":
                            if GRID1:
                                algorithm_completed = True
                                reset_grid(grid, start, end)  # Reset the grid before running the algorithm
                                for row in grid:
                                    for spot in row:
                                        spot.update_neighbors(grid)
                                algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.breadth_first_search(
                                    lambda: draw(win, grid, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE), grid, start, end,
                                    chosen_heuristic, delay_time)
                                nodes_entry.set_text(str(expanded_nodes))
                                steps_entry.set_text(str(steps))
                                length_entry.set_text(str(path_length))
                                time_entry.set_text(f"{elapsed_time:.2f} s")
                        elif drop_down.selected_option == "Depth-First-Search":
                            if GRID1:
                                algorithm_completed = True
                                reset_grid(grid, start, end)  # Reset the grid before running the algorithm
                                for row in grid:
                                    for spot in row:
                                        spot.update_neighbors(grid)
                                algorithm_completed, expanded_nodes, steps, path_length, elapsed_time = algorithms.depth_first_search(
                                    lambda: draw(win, grid, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE), grid, start, end,
                                    chosen_heuristic, delay_time)
                                nodes_entry.set_text(str(expanded_nodes))
                                steps_entry.set_text(str(steps))
                                length_entry.set_text(str(path_length))
                                time_entry.set_text(f"{elapsed_time:.2f} s")
                    else:
                        algorithm_error_label.show()


                if event.ui_element == grid_nr_btn:
                    grids_window.show()
                    grid_nr_error_label.hide()

                if event.ui_element == colors_btn:
                    colors_window.show()

                if event.ui_element == closed_node_btn:
                    current_colour = pygame.Color(0, 0, 0)
                    closed_node_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                         manager = manager2,
                                                         window_title='Change colour',
                                                         initial_colour=current_colour)

                if event.ui_element == open_node_btn:
                    current_colour = pygame.Color(0, 0, 0)
                    open_node_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                         manager = manager2,
                                                         window_title='Change colour',
                                                         initial_colour=current_colour)
                if event.ui_element == path_btn:
                    current_colour = pygame.Color(0, 0, 0)
                    path_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                         manager = manager2,
                                                         window_title='Change colour',
                                                         initial_colour=current_colour)

                if event.ui_element == settings_btn:
                    GRID1 = True
                    GRID2 = False
                    GRID3 = False
                    GRID4 = False



                if event.ui_element == romanian_button:
                    manager.set_locale('ro')
                    manager2.set_locale('ro')

                if event.ui_element == english_button:
                    manager.set_locale('en')
                    manager2.set_locale('en')

                if event.ui_element == bg_mode_button:
                    change_bg()
                    manager.draw_ui(screen)
                    grid = make_grid(ROWS, width)
                    grid2_1 = make_grid(ROWS, GRID_WIDTH2)
                    grid2_2 = make_grid(ROWS, GRID_WIDTH2)
                    grid3_1 = make_grid(ROWS, GRID_WIDTH3)
                    grid3_2 = make_grid(ROWS, GRID_WIDTH3)
                    grid3_3 = make_grid(ROWS, GRID_WIDTH3)
                    grid4_1 = make_grid(ROWS, GRID_WIDTH4)
                    grid4_2 = make_grid(ROWS, GRID_WIDTH4)
                    grid4_3 = make_grid(ROWS, GRID_WIDTH4)
                    grid4_4 = make_grid(ROWS, GRID_WIDTH4)

            if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
                if event.ui_element == closed_node_picker:
                    global RED
                    RED = event.colour
                    update_color(rgb_to_hex(event.colour), "closed")

                elif event.ui_element == open_node_picker:
                    global GREEN
                    GREEN = event.colour
                    update_color(rgb_to_hex(event.colour), "open")

                elif event.ui_element == path_picker:
                    global PURPLE
                    PURPLE = event.colour
                    update_color(rgb_to_hex(event.colour), "path")

            manager.process_events(event)
            manager2.process_events(event)

        manager.update(time_delta)
        manager2.update(time_delta)

        screen.fill(BG_COLOR)
        manager.draw_ui(screen)

        if GRID1:
            draw(win, grid, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE)
            #algorithm_completed = False

        if GRID2:
            draw(win, grid2_1, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE2_1)
            draw(win, grid2_2, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE2_2)
            algorithm_completed = False

        if GRID3:
            draw(win, grid3_1, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE3_1)
            draw(win, grid3_2, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE3_2)
            draw(win, grid3_3, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE3_3)
            algorithm_completed = False

        if GRID4:
            draw(win, grid4_1, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE4_1)
            draw(win, grid4_2, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE4_2)
            draw(win, grid4_3, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE4_3)
            draw(win, grid4_4, ROWS, width, time_elapsed, algorithm_completed, GRID_SURFACE4_4)
            algorithm_completed = False


        manager2.draw_ui(screen)
        pygame.display.update()


    pygame.quit()

main(screen, GRID_WIDTH)
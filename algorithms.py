import math
from collections import deque
from enum import Enum, auto
import pygame
from queue import PriorityQueue
from queue import Queue
import time
import settings

SHOW_ARROWS = settings.SHOW_ARROWS
DIAGONAL = settings.DIAGONAL
mode = settings.mode

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



def axial_to_cube(row, col):
    x = col
    z = row - (col - (col & 1)) // 2
    y = -x - z
    return x, y, z

class Heuristic(Enum):
    MANHATTAN = auto()
    EUCLIDEAN = auto()
    OCTILE = auto()
    CHEBYSHEV = auto()

def heuristic(heuristic_type):
    if mode == "hexagon":
        return lambda p1, p2: (abs(axial_to_cube(p1[0], p1[1])[0] - axial_to_cube(p2[0], p2[1])[0]) + abs(
            axial_to_cube(p1[0], p1[1])[1] - axial_to_cube(p2[0], p2[1])[1]) + abs(
            axial_to_cube(p1[0], p1[1])[2] - axial_to_cube(p2[0], p2[1])[2])) // 2
    elif mode == "square" or mode == "triangle":
        if heuristic_type == Heuristic.MANHATTAN:
            return lambda p1, p2: abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
        elif heuristic_type == Heuristic.EUCLIDEAN:
            return lambda p1, p2: math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
        elif heuristic_type == Heuristic.OCTILE:
            return lambda p1, p2: max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1])) + (math.sqrt(2) - 1) * min(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
        elif heuristic_type == Heuristic.CHEBYSHEV:
            return lambda p1, p2: max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))
        else:
            raise ValueError("Invalid heuristic type")



def reconstruct_path(came_from, current, draw, start):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current)
        if current != start:
            current.make_path()
        draw()
    return len(path)

def dijkstra(draw, grid, start, end, heuristic_function, delay_time):
    count = 0
    steps = 0
    start_time = time.time()
    expanded_nodes = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            elapsed_time = time.time() - start_time
            path_length = reconstruct_path(came_from, end, draw, start)
            end.make_end()
            print(f"Nodes expanded: {expanded_nodes}")
            print(f"Steps: {steps}")
            print(f"Path length: {path_length}")
            print(f"Time taken: {elapsed_time:.4f} seconds")
            return True, expanded_nodes, steps, path_length, elapsed_time

        for neighbor in current.neighbors:
            steps += 1
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                neighbor.predecessor = current
                neighbor.arrow_color = GREY
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    expanded_nodes += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        pygame.time.delay(delay_time)

        if current != start:
            current.make_closed()

    return False, 0, 0, 0, 0


def best_first_search(draw, grid, start, end, h, delay_time):
    count = 0
    steps = 0
    start_time = time.time()
    expanded_nodes = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    h_score = {spot: float("inf") for row in grid for spot in row}
    h_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            elapsed_time = time.time() - start_time
            path_length = reconstruct_path(came_from, end, draw, start)
            end.make_end()
            print(f"Nodes expanded: {expanded_nodes}")
            print(f"Steps: {steps}")
            print(f"Path length: {path_length}")
            print(f"Time taken: {elapsed_time:.4f} seconds")
            return True, expanded_nodes, steps, path_length, elapsed_time

        for neighbor in current.neighbors:
            steps += 1
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                neighbor.predecessor = current
                neighbor.arrow_color = GREY
                g_score[neighbor] = temp_g_score
                h_score[neighbor] = h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    expanded_nodes += 1
                    open_set.put((h_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        pygame.time.delay(delay_time)

        if current != start:
            current.make_closed()

    return False, 0, 0, 0, 0


def breadth_first_search(draw, grid, start, end, h, delay_time):
    count = 0
    steps = 0
    start_time = time.time()
    expanded_nodes = 0
    open_set = deque()  # Use deque() instead of PriorityQueue()
    open_set.append(start)  # Replace .put() with .append()
    came_from = {}

    visited = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.popleft()  # Replace .get() with .popleft()

        if current == end:
            elapsed_time = time.time() - start_time
            path_length = reconstruct_path(came_from, end, draw, start)
            end.make_end()
            print(f"Nodes expanded: {expanded_nodes}")
            print(f"Steps: {steps}")
            print(f"Path length: {path_length}")
            print(f"Time taken: {elapsed_time:.4f} seconds")
            return True, expanded_nodes, steps, path_length, elapsed_time

        for neighbor in current.neighbors:
            steps += 1
            if neighbor not in visited:
                neighbor.predecessor = current
                neighbor.arrow_color = GREY
                count += 1
                expanded_nodes += 1
                came_from[neighbor] = current
                open_set.append(neighbor)
                visited.add(neighbor)
                neighbor.make_open()

        draw()
        pygame.time.delay(delay_time)

        if current != start:
            current.make_closed()

    return False, 0, 0, 0, 0


def depth_first_search(draw, grid, start, end, h, delay_time):
    count = 0
    steps = 0
    start_time = time.time()
    expanded_nodes = 0
    open_set = [start]  # Use list as a stack for DFS
    came_from = {}

    visited = {start}

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.pop()  # Use .pop() for the stack (DFS)

        if current == end:
            elapsed_time = time.time() - start_time
            path_length = reconstruct_path(came_from, end, draw, start)
            end.make_end()
            print(f"Nodes expanded: {expanded_nodes}")
            print(f"Steps: {steps}")
            print(f"Path length: {path_length}")
            print(f"Time taken: {elapsed_time:.4f} seconds")
            return True, expanded_nodes, steps, path_length, elapsed_time

        for neighbor in current.neighbors:
            steps += 1
            if neighbor not in visited:
                neighbor.predecessor = current
                neighbor.arrow_color = GREY
                count += 1
                expanded_nodes += 1
                came_from[neighbor] = current
                open_set.append(neighbor)
                visited.add(neighbor)
                neighbor.make_open()

        draw()
        pygame.time.delay(delay_time)

        if current != start:
            current.make_closed()

    return False, 0, 0, 0, 0



def astar(draw, grid, start, end, heuristic_function, delay_time):
    count = 0
    steps = 0
    start_time = time.time()
    expanded_nodes = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic_function(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            elapsed_time = time.time() - start_time
            path_length = reconstruct_path(came_from, end, draw, start)
            end.make_end()
            print(f"Nodes expanded: {expanded_nodes}")
            print(f"Steps: {steps}")
            print(f"Path length: {path_length}")
            print(f"Time taken: {elapsed_time:.4f} seconds")
            return True, expanded_nodes, steps, path_length, elapsed_time

        for neighbor in current.neighbors:
            steps += 1
            if DIAGONAL and abs(neighbor.row - current.row) == 1 and abs(neighbor.col - current.col) == 1:
                temp_g_score = g_score[current] + math.sqrt(2)
            else:
                temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                neighbor.predecessor = current
                neighbor.arrow_color = GREY
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic_function(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    expanded_nodes += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()
        pygame.time.delay(delay_time)

        if current != start:
            current.make_closed()

    return False, 0, 0, 0, 0
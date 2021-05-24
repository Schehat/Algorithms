import pygame
import os
from queue import PriorityQueue

pygame.init()
pygame.font.init()
font = pygame.font.SysFont("timesnewroman", 50)
os.environ['SDL_VIDEO_CENTERED'] = '1'
clock = pygame.time.Clock()
FPS = 60

WINDOW_SIZE = (600, 600)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("A* Star Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
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

    def is_obstacle(self):
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

    def make_opened(self):
        self.color = GREEN

    def make_obstacle(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y, self.width, self.width))

    def update(self, grid):
        self.neighbors = []

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():  # down
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():  # up
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():  # left
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle():  # right
            self.neighbors.append(grid[self.row][self.col + 1])

    '''def __lt__(self, other):
        return False'''


# horizontal and vertical distance of both nodes
def h(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    return abs(x2 - x1) + abs(y2 - y1)


def reconstruct_path(came_from, end, grid, rows):
    while end in came_from:
        end = came_from[end]
        end.make_path()
        draw(grid, rows)


def algorithm(grid, start, end, rows):
    count = 0  # needed to sort nodes with same f score
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}  # needed to make the shortest path
    g_score = {node: float("inf") for i in grid for node in i}
    g_score[start] = 0
    f_score = {node: float("inf") for i in grid for node in i}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, grid, rows)
            end.make_end()  # end node keeps his color same for start
            start.make_start()
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
                    neighbor.make_opened()

        draw(grid, rows)

        if current != start:
            current.make_closed()

    # no path
    if current != end:
        draw_text()


def draw_text():
    text = font.render("No Path Found", 1, RED)
    WINDOW.blit(text, (int(WINDOW_SIZE[0] / 2 - text.get_width() / 2), 100))
    pygame.display.update()
    pygame.time.delay(2000)


def make_grid(rows):
    grid = []
    gap = WINDOW_SIZE[0] // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw(grid, rows):
    WINDOW.fill(WHITE)

    for i in grid:
        for j in i:
            j.draw()

    gap = int(WINDOW_SIZE[0] / rows)
    for i in range(rows):
        pygame.draw.line(WINDOW, GREY, (0, i * gap), (WINDOW_SIZE[0], i * gap))  # horizontal
        for j in range(rows):
            pygame.draw.line(WINDOW, GREY, (j * gap, 0), (j * gap, WINDOW_SIZE[0]))  # vertical

    pygame.display.update()


def get_clicked_position(rows, pos):
    gap = WINDOW_SIZE[0] / rows
    x, y = pos

    row = int(y / gap)
    col = int(x / gap)

    return row, col


def main():
    rows = 50
    grid = make_grid(rows)

    start = None
    end = None

    run = True
    algorithm_start = False
    while run:
        clock.tick(FPS)
        draw(grid, rows)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if pygame.mouse.get_pressed()[0]:  # left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(rows, pos)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    node.make_start()

                elif not end and node != start:
                    end = node
                    node.make_end()

                elif node != start and node != end:
                    node.make_obstacle()

            elif pygame.mouse.get_pressed()[2]:  # right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(rows, pos)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if pygame.key.get_pressed()[pygame.K_SPACE] and start and end:
                for i in grid:
                    for j in i:
                        j.update(grid)

                algorithm(grid, start, end, rows)

            if pygame.key.get_pressed()[pygame.K_c] and not algorithm_start:
                start = None
                end = None
                grid = make_grid(rows)


main()

from queue import PriorityQueue
import pygame
pygame.init()

WIDTH = 800
HEIGHT = 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Search Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, height, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.midX = self.x + width // 2
        self.midY = self.y + height // 2
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.height = height
        self.total_rows = total_rows
        self.total_cols = total_cols

    def get_grid_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == TURQUOISE

    def is_goal(self):
        return self.color == GOLD

    def reset(self):
        self.color = WHITE

    def set_open(self):
        self.color = GREEN

    def set_closed(self):
        self.color = RED

    def set_obstacle(self):
        self.color = BLACK

    def set_start(self):
        self.color = TURQUOISE

    def set_goal(self):
        self.color = GOLD

    def set_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

    def update_neighbors(self, grid):
        self.neightbors = []
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col])
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])
        # RIGHT
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])
        # DIAGONALS
        if self.row > 0 and self.col > 0 and not grid[self.row - 1][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col - 1])
        if self.row > 0 and self.col < self.total_cols - 1 and not grid[self.row - 1][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col + 1])
        if self.row < self.total_rows - 1 and self.col > 0 and not grid[self.row + 1][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col - 1])
        if self.row < self.total_rows - 1 and self.col < self.total_cols - 1 and not grid[self.row + 1][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col + 1])

    def __lt__(self, other):
        return False


def heur(n1, n2):
    return abs(n1.midX - n2.midX) + abs(n1.midY - n2.midY)


def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()


def astar(draw, grid, start, goal):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_cost = {node: float("inf") for row in grid for node in row}
    g_cost[start] = 0
    f_cost = {node: float("inf") for row in grid for node in row}
    f_cost[start] = heur(start, goal)
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == goal:
            reconstruct_path(came_from, goal, draw)
            goal.set_goal()
            return True

        for neighbor in current.neighbors:
            temp_g_cost = g_cost[current] + 1
            if temp_g_cost < g_cost[neighbor]:
                came_from[neighbor] = current
                g_cost[neighbor] = temp_g_cost
                f_cost[neighbor] = temp_g_cost + \
                    heur(neighbor, goal)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_cost[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()

        draw()

        if current != start:
            current.set_closed()
    return False


def create_grid(rows, columns, width, height):
    grid = []
    x_step = width // columns
    y_step = height // rows
    for i in range(rows):
        grid.append([])
        for j in range(columns):
            node = Node(i, j, x_step, y_step, rows, columns)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, columns, width, height):
    x_step = width // columns
    y_step = height // rows

    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * y_step), (width, i * y_step))
    for j in range(columns):
        pygame.draw.line(win, GREY, (j * x_step, 0), (j * x_step, height))


def draw(win, grid, rows, cols, width, height):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, cols, width, height)
    pygame.display.update()


def find_grid_pos(pos, rows, columns, width, height):
    x_step = width // columns
    y_step = height // rows

    y, x = pos

    row = y // y_step
    col = x // x_step
    return row, col


def main(win, width, height):
    ROWS = 25
    COLS = 25
    grid = create_grid(ROWS, COLS, width, height)

    start = None
    goal = None

    crashed = False
    while not crashed:
        draw(win, grid, ROWS, COLS, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True
            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                r, c = find_grid_pos(mouse_pos, ROWS, COLS, width, height)
                node = grid[r][c]
                if not start:
                    start = node
                    start.set_start()
                elif not goal:
                    goal = node
                    goal.set_goal()
                elif node != start and node != goal:
                    node.set_obstacle()
            elif pygame.mouse.get_pressed()[2]:
                mouse_pos = pygame.mouse.get_pos()
                r, c = find_grid_pos(mouse_pos, ROWS, COLS, width, height)
                node = grid[r][c]
                node.reset()
                if node == start:
                    start = None
                elif node == goal:
                    goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and goal:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    astar(lambda: draw(win, grid, ROWS, COLS,
                                       width, height), grid, start, goal)
                if event.key == pygame.K_c:
                    start = None
                    goal = None
                    grid = create_grid(ROWS, COLS, width, height)
    pygame.quit()


main(WIN, WIDTH, HEIGHT)

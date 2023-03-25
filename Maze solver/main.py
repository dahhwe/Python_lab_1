from random import shuffle, randint

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def make_maze(maze_width=20, maze_height=20):
    vis = [[0] * maze_width + [1] for _ in range(maze_height)] + [[1] * (maze_width + 1)]
    ver = [["|  "] * maze_width + ['|'] for _ in range(maze_height)] + [[]]
    hor = [["+--"] * maze_width + ['+'] for _ in range(maze_height + 1)]

    # Add entry and exit points
    hor[0][0] = "+  "
    hor[maze_height][maze_width - 1] = "+  "

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(0, 0)

    # Check if there is a route from entry to exit
    visited = [[False for _ in range(maze_width)] for _ in range(maze_height)]

    def dfs(x, y):
        if x < 0 or x >= maze_width or y < 0 or y >= maze_height or visited[y][x]:
            return False
        visited[y][x] = True
        if x == maze_width - 1 and y == maze_height - 1:
            return True
        if hor[y][x] == "+  " and dfs(x, y - 1):
            return True
        if hor[y + 1][x] == "+  " and dfs(x, y + 1):
            return True
        if ver[y][x] == "   " and dfs(x - 1, y):
            return True
        if ver[y][x + 1] == "   " and dfs(x + 1, y):
            return True
        return False

    if not dfs(0, 0):
        # If there is no route from entry to exit, create one by removing walls randomly
        while not dfs(0, 0):
            x = randint(0, maze_width - 1)
            y = randint(0, maze_height - 1)
            d = randint(0, 3)
            if d == 0:
                hor[y][x] = "+  "
            elif d == 1:
                hor[y + 1][x] = "+  "
            elif d == 2:
                ver[y][x] = "   "
            else:
                ver[y][x + 1] = "   "
            visited = [[False for _ in range(maze_width)] for _ in range(maze_height)]

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    return s


def draw_maze(maze_str):
    block_size = 20
    width = max(map(len, maze_str.split('\n')))
    height = len(maze_str.split('\n'))

    screen = pygame.display.set_mode((width * block_size // 2, height * block_size // 2))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(WHITE)

        x, y = 0, 0
        for row in maze_str.split('\n'):
            for ch in row:
                if ch == '+':
                    pygame.draw.rect(screen, BLACK, (x, y, block_size / 2, block_size / 2))
                elif ch == '-':
                    pygame.draw.rect(screen, BLACK, (x, y, block_size / 2,
                                                     block_size / 2))
                elif ch == '|':
                    pygame.draw.rect(screen, BLACK, (x, y, block_size / 2,
                                                     block_size / 2))
                x += block_size / 2
            x = 0
            y += block_size / 2

        pygame.display.flip()
        clock.tick(144)


if __name__ == '__main__':
    pygame.init()
    width = input("enter width:")
    height = input("Enter height:")
    maze_str = make_maze(int(width), int(height))
    print(maze_str)
    draw_maze(maze_str)


import colorama
import readchar
import random

colorama.just_fix_windows_console()

w, h = 10, 10
m = 10

up = lambda x: f"\033[{x}A"

board = [[False for _ in range(w)] for _ in range(h)]
fog = [[True for _ in range(w)] for _ in range(h)]
flags = [[False for _ in range(w)] for _ in range(h)]

first_move = True

cur = [0, 0]

def print_board():
    for y, i in enumerate(board):
        for x, j in enumerate(i):
            print("[" if cur[0] == x and cur[1] == y else " ", end="")
            
            if flags[y][x]:
                if not board[y][x] and not fog[y][x]:
                    print("\033[31mF\033[0m", end="")
                else:
                    print("\033[33mF\033[0m", end="")
            else:
                if not fog[y][x]:
                    if j: print("\033[31m#\033[0m", end="")
                    else: print(" " if count_neighbours([x, y]) == 0 else f"{str(count_neighbours([x, y]))}", end="")
                else: print(".", end="")

            print("]" if cur[0] == x and cur[1] == y else " ", end="")
        print()

def move_cursor(where):
    global cur
    where = {"w": 0, "a": 1, "s": 2, "d": 3, readchar.key.UP: 0, readchar.key.LEFT: 1, readchar.key.DOWN: 2, readchar.key.RIGHT: 3}[where]

    if where == 0:
        if cur[1] > 0: cur[1] -= 1
    if where == 1:
        if cur[0] > 0: cur[0] -= 1
    if where == 2:
        if cur[1] < h - 1: cur[1] += 1
    if where == 3:
        if cur[0] < w - 1: cur[0] += 1

def count_neighbours(cur):
    neighbours = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i != 0 or j != 0:
                if cur[1] + i >= 0 and cur[0] + j >= 0 and cur[1] + i < w and cur[0] + j < h:
                    if board[cur[1] + i][cur[0] + j]: neighbours += 1

    return neighbours

def randomize_mines():
    for _ in range(m):
        x, y = random.randint(0, w - 1), random.randint(0, h - 1)
        while board[y][x]:
            x, y = random.randint(0, w - 1), random.randint(0, h - 1)

        board[y][x] = True

def open_all_mines():
    global fog
    for y, i in enumerate(board):
        for x, j in enumerate(i):
            if j: fog[y][x] = False

get_is_mine = lambda cur: board[cur[1]][cur[0]]
get_is_fog = lambda cur: fog[cur[1]][cur[0]]
get_is_flag = lambda cur: flags[cur[1]][cur[0]]

def open_on(cur):
    if not (cur[0] >= 0 and cur[1] >= 0 and cur[0] < h and cur[1] < w): return
    if not get_is_fog(cur): return
    
    fog[cur[1]][cur[0]] = False

    if count_neighbours(cur) == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                open_on([cur[0] + i, cur[1] + j])

def all_flags_are_mines():
    flag_count = 0
    for y, i in enumerate(flags):
        for x, j in enumerate(i):
            if j:
                if board[y][x]:
                    flag_count += 1
                else:
                    flag_count -= 1
    if flag_count == m:
        return True
    return False

def add_flag():
    global flags

    flags[cur[1]][cur[0]] = not flags[cur[1]][cur[0]]
    if all_flags_are_mines():
        print(up(h), end="")
        print_board()
        print("-> You won! :D")
        exit()

def open_fog():
    global fog
    first_move = False
    
    if board[cur[1]][cur[0]]:
        if first_move: # sneakily move mine somewhere else
            x, y = random.randint(0, w - 1), random.randint(0, h - 1)
            
            while board[y][x]:
                x, y = random.randint(0, w - 1), random.randint(0, h - 1)
            
            board[y][x] = True
            board[cur[1]][cur[0]] = False

        open_all_mines()
        print(up(h), end="")
        print_board()
        print("-> You lose! :(")
        exit()

    open_on(cur)

if __name__ == "__main__":
    print("=> Config:")
    print(f"->     Size: {w}x{h}; Mines: {m}")
    print("=> Controls:")
    print("->     [WASD] or [v]/[^]/[<]/[>] - move the cursor")
    print("->     [Space] - Open a cell")
    print("->     [F] - Place a flag")
    print("->     [Q] - Exit\n")
    randomize_mines()
    while True:
        print_board()
        key = readchar.readkey()

        if key in "wasd" or key in (readchar.key.DOWN, readchar.key.UP, readchar.key.LEFT, readchar.key.RIGHT):
            move_cursor(key)
        if key == readchar.key.SPACE:
            open_fog()
        if key == "f":
            add_flag()
        if key == "q": exit()
        
        print(up(h), end="")


import colorama
import readchar
import random
import sys

colorama.just_fix_windows_console()

w, h = 10, 10
m = 10

up = lambda x: f"\033[{x}A"

first_move = True

cur = [0, 0]

def print_board():
    for y, i in enumerate(board):
        for x, j in enumerate(i):
            print("[" if cur[0] == x and cur[1] == y else " ", end="")
            
            if flags[y][x]:
                if not board[y][x] and (not fog[y][x] or debug):
                    print("\033[31mF\033[0m", end="")
                else:
                    print("\033[33mF\033[0m", end="")
            else:
                if not fog[y][x]:
                    if j: print("\033[31m#\033[0m", end="")
                    else: print(" " if count_neighbours([x, y]) == 0 else f"{str(count_neighbours([x, y]))}", end="")
                else:
                    if debug:
                        print("\033[31m.\033[0m" if board[y][x] else ".", end="")
                    else:
                        print(".", end="")

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
                if cur[1] + i >= 0 and cur[0] + j >= 0 and cur[1] + i < h and cur[0] + j < w:
                    
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
    if not (cur[0] >= 0 and cur[1] >= 0 and cur[0] < w and cur[1] < h): return
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

def print_usage():
    print(f"=> Usage: {program} [-h] [-u] [-d] [<flag> <value>]")
    print("-> Flags:")
    print("->     -w <int>      Set board width")
    print("->     -h <int>      Set board height")
    print("->     -m <int>      Set mine count")

def print_help():
    print("=> How to play minesweeper:\n"
          "-> You are given a board, with randomly put mines in it.\n"
          "-> Your objective is to find all these mines and flag\n"
          "-> them. Remember that your first click is not a mine.\n"
          "-> Numbers on empty cells indicate how many mines around\n"
          "-> it (8x8 square, if cell is empty there are no mines).\n"
          "-> For example lets look at this situation:\n"
          " > |           |\n"
          " > |     1  1  |\n"
          " > |     1 [.] |\n"
          "-> We can for sure say that there is a mine at cursor,\n"
          "-> because there are exactly one mine around the cell\n"
          "-> at the center. To flag the cell press [F] - this will\n"
          "-> place a flag at position of cursor. Also - if flag is\n"
          "-> red it means that this cell is already opened and\n"
          "-> there are no mine in it, so you can safely remove it.\n"
          "-> Thats all - now just start a program without any\n"
          "-> arguments to start a standart (10x10#10) game.")

def isint(string):
    try:
        int(string)
        return True
    except:
        return False

debug = False

if __name__ == "__main__":
    program = sys.argv.pop(0)

    while len(sys.argv) > 0:
        flag = sys.argv.pop(0)

        if flag == "-h":
            print_help()
            exit()
        
        if flag == "-u":
            print_usage()
            exit()

        if flag == "-d":
            debug = True
            continue

        if len(sys.argv) == 0:
            print("=> Error: Got flag but did not got any value")
            print_usage()
            exit(1)
        
        if flag == "-w":
            w = sys.argv.pop(0)
            if not isint(w):
                print(f"=> Error: \"{w}\" is not a proper integer")
                exit(1)
            w = int(w)
        elif flag == "-h":
            h = sys.argv.pop(0)
            if not isint(h):
                print(f"=> Error: \"{h}\" is not a proper integer")
                exit(1)
            h = int(h)
        elif flag == "-m":
            m = sys.argv.pop(0)
            if not isint(m):
                print(f"=> Error: \"{m}\" is not a proper integer")
                exit(1)
            m = int(m)

        else:
            print(f"=> Error: Unknown flag \"{flag}\"")
            print_usage()
            exit()
    
    board = [[False for _ in range(w)] for _ in range(h)]
    fog = [[True for _ in range(w)] for _ in range(h)]
    flags = [[False for _ in range(w)] for _ in range(h)]

    print("=> Config:")
    print(f"->     Size: {w}x{h}; Mines: {m}")
    if debug: print("->     ~~ DEBUG MODE ~~")
    print("=> Controls:")
    print("->     [WASD] or [v]/[^]/[<]/[>] - Move the cursor")
    print("->     [Space] - Open a cell")
    print("->     [F] - Place a flag")
    print("->     [Q] - Exit\n")
    randomize_mines()
    while True:
        print_board()
        try: key = readchar.readkey()
        except KeyboardInterrupt: exit()

        if key in "wasd" or key in (readchar.key.DOWN, readchar.key.UP, readchar.key.LEFT, readchar.key.RIGHT):
            move_cursor(key)
        if key == readchar.key.SPACE:
            open_fog()
        if key == "f":
            add_flag()
        if key == "q": exit()
        
        print(up(h), end="")


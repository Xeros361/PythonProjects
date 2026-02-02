import random
print("Minesweeper")
while True:
    rows = int(input("Numbers of rows: "))
    cols = int(input("Numbers of columns: "))
    lvl = input("Difficulty (Easy, Medium, Hard): ")
    if 100 > rows > 0 and 100 > cols > 0 and lvl.lower() in ['easy', 'medium', 'hard']:
        break
mines = 0
if lvl.lower() == 'easy':
    mines = (rows * cols) * 0.12
elif lvl.lower() == 'medium':
    mines = (rows * cols) * 0.16
elif lvl.lower() == 'hard':
    mines = (rows * cols) * 0.22
if mines == 0:
    mines = 1
mines = int(mines)
flags = int(mines)

fields = (rows * cols) - mines
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8]
board = [[0] * cols for _ in range(rows)]
b = [["•"] * cols for _ in range(rows)]





def place_mines():
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == "B":
                continue
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < rows and 0 <= ny < cols:
                        if board[nx][ny] == "B":
                            count += 1
            board[x][y] = count


def reveal(x, y):
    if not (0 <= x < rows and 0 <= y < cols):
        return
    if b[x][y] != "•":
        return
    if board[x][y] == "B":
        return
    if b[x][y] == "F":
        return

    b[x][y] = board[x][y]

    if board[x][y] == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    reveal(x + dx, y + dy)

def check_win():
    cn = 0
    for x in range(rows):
        for y in range(cols):
            if b[x][y] in nums:
                cn += 1
    if cn == fields:
        return True
    return False

def generate_first_mines(fx, fy):
    all_fields = [(i, j) for i in range(rows) for j in range(cols)]

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = fx + dx, fy + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if (nx, ny) in all_fields:
                    all_fields.remove((nx, ny))
    mine_positions = random.sample(all_fields, mines)

    for (mx, my) in mine_positions:
        board[mx][my] = "B"

    place_mines()

    reveal(fx, fy)

first_click = True

while True:
    print("")
    if check_win():
        print("You won.")
        print("")
        for x in range(len(b)):
            for y in range(len(b[x])):
                print(b[x][y], end=" ")
            print("")
        break
    print(f"Flags left: {flags}")
    print("")
    print("", end="    ")
    for i in range(cols):
        if i > 9:
            print(str(i)[1], end=" ")
            continue
        print(i, end=" ")
    print("")
    for x in range(len(b)):
        for y in range(len(b[x])):
            if y == 0:
                if len(str(x)) == 1:
                    print("", x, end="  ")
                elif len(str(x)) == 2:
                    print(x, end="  ")

            print(b[x][y], end=" ")
        print("")
    print("")
    user_input = input("Row, Column, Action (x y ('c' click, 'f' flag)): ").split()

    if len(user_input) != 3:
        print("Invalid input.")
        continue

    x_str, y_str, a = user_input

    try:
        x = int(x_str)
        y = int(y_str)
    except ValueError:
        print("Row and column must be numbers.")
        continue

    if a.lower() not in ['c', 'f']:
        print("Action must be 'c' (click) or 'f' (flag).")
        continue

    if (x < 0 or x >= rows) or (y < 0 or y >= cols):
        print("Out of bounds.")
        continue

    if first_click and a.lower() == 'c':
        generate_first_mines(x, y)
        first_click = False

    if a.lower() == 'f':
        if b[x][y] == '•':
            b[x][y] = 'F'
            flags -= 1
        elif b[x][y] == 'F':
            b[x][y] = "•"
            flags += 1
    elif a.lower() == 'c':
        if b[x][y] == "F":
            print("")
            print("Remove the flag.")
            continue
        if board[x][y] == "B":
            print("")
            print("Bomb. You lost.")
            print("")
            for x in range(len(b)):
                for y in range(len(b[x])):
                    if board[x][y] == 'B':
                        b[x][y] = 'B'

            for x in range(len(b)):
                for y in range(len(b[x])):
                    print(b[x][y], end=" ")
                print("")
            break

        reveal(x, y)
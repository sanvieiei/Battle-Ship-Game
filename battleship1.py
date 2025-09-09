'''
Name: Sanvi Takyar & Eric Li
Date: April 7, 2025
Program details: Battle ship game
'''
import random

def validate_first(turn):
    '''Takes in the parameter turn.
    Will make sure that the user enters a valid response to the question who goes first.
    Returns True or False.'''
    if turn == "Y" or turn =="N":
        return True
    else:
        return False
       
def place_ships(board_size):
    '''Places te ships on the board.
    Takes in the parameter board size.
    Will place the ships randomly on the board for both the user and the computer.'''
    user_ships = {}
    computer_ships = {}
    for i in range(3):
        row = random.randrange(board_size)
        col = random.randrange(board_size)
        position = (row,col)
       
        if position not in user_ships.values():
            ship_id = "user_ship_"+str(i)
            user_ships[ship_id] = position
       
    for i in range(3):
        row = random.randrange(board_size)
        col = random.randrange(board_size)
        position = (row,col)

        if (position not in user_ships.values()) and (position not in computer_ships.values()):
            ship_id = "computer_ship"+str(i)
            computer_ships[ship_id] = position
    return user_ships, computer_ships

def make_user_move(board, board_size,computer_ships):
    valid_move = False
    while not valid_move:
        rows = int(input("Enter the row where you would like to enter your missile: "))
        cols = int(input("Enter the column where you would like to enter your missile: "))
        try:
            if (0<=rows<board_size) and (0<=cols<board_size):
                hit = (rows,cols)
                if hit in computer_ships.values():
                    board[rows][cols] = "X"
                    for key in computer_ships.keys():
                        if computer_ships[key] == hit:
                            del computer_ships[key]
                            break
                    valid_move = True
                else:
                    board[rows][cols] = "O"
                    valid_move = True
            else:
                print("Invalid input")
        except ValueError:
            print("Invalid Input.")

def make_computer_move(board, board_size, user_ships):
   while True:
       row = random.randrange(board_size)
       col = random.randrange(board_size)
       hit = (row,col)
       if board[row][col] == ' ':
           if hit in user_ships.values():
                board[row][col] = "X"
                for key in user_ships.keys():
                    if user_ships[key] == hit:
                        del user_ships[key]
                        break
                break
           else:
               board[row][col] = "O"
               break
           
       
def validate_board_size(board_size):
    '''Takes in the board_size parameter.
    Will validate the board size and make sure it is within the '''
    if 6<=(board_size)<=10:
        return True
    else:
        return False

def gameboard_squares(board_size):
    '''Makes gameboard'''
    rows, columns = board_size, board_size
    board = []
    for _ in range(rows):
        board.append([" "]*columns)
    return board

def display_board(board, user_ship):
    print("W E L C O M E  T O  B A T T L E S H I P:")
    print("    ", end="")
    for header in range(len(board[0])):
        print(" %2d  " % (header), end="")
    print()

    for row in range(len(board)):
        row_str = "%2d |" % row
        col_str = "   +"
        for col in range(len(board[row])):
           ship = (row,col)
           if ship in user_ship.values():
               board[row][col] = "U"
           row_str += " %2s |" % board[row][col]
           col_str += "----+"
        print(row_str)
        print(col_str)
       
def place_mines(board_size, ships):
    '''Randomly place 1-3 hidden mines around the map.'''
    mine_count = random.randint(1, 3)
    mines = {}
    while len(mines) < mine_count:
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        position = (row, col)
           
        if position not in mines:
            mine_type = random.choice(["bomb", "cross"])
            mines[position] = mine_type
           
    return mines

def mine_radius(mine_type):
    '''Finds the blocks that will be affected by the mine's explosion.'''
    if mine_type == "bomb":
        return [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    if mine_type == "cross":
        return [(-1, 0), (0, -1), (0, 1), (1, 0)]
   
def mine_explosion(mine_type, board, user_ships, computer_ships):
    '''Explodes the mine and destroys any ship in the radius.'''
    row, col = mine_position
    board[row][col] = "*"
    radius = mine_radius(mine_type)
   
def main():
    '''Mainline Logic.'''
    while True:
        board_size = int(input("Enter a value between (6 to 10) to initalize the board size: "))
        if validate_board_size(board_size):
            board = gameboard_squares(board_size)
            break
   
    user_ships, computer_ships = place_ships(board_size)
    display_board(board,user_ships)

    while True:
        turn = ((input("Do you want to go first (enter Y or N): ")).upper()).strip()
        if validate_first(turn):
            break
        else:
            print("Invalid Input.")

    while True:
        if turn == "Y":
            make_user_move(board, board_size,computer_ships)
            display_board(board, user_ships)
            turn = "N"  
        else:
            make_computer_move(board, board_size,user_ships)
            display_board(board, user_ships)
            turn = "Y"
main()
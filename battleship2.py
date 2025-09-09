'''
Name: Sanvi Takyar & Eric Li
Date: April 13, 2025
This program will play a battle ship game between the user and the computer. 
The user can choose the board dimensions ranging from 6x6 to 10x10.
The user's ships and the computer's ships will be randomly placed on the board.
Both parties will take turn shooting missiles to hit the opposing side's ships.
If a missile hits, the ship hit will sink. Mines will also be randomly placed on the board. 
If a mine is hit, there is two ways it can explode. 
If a ship is in the affected area of the mine, it will be destroyed.
'''
import random

def validate_first():
    '''Validates who takes the first turn in the game.
 Takes no parameters.
 Prompts the user for input and ensures it is 'Y' or 'N'.
 Returns the turn choice (str).'''
    
    while True:
        #Makes sure that the user input is either "Y"/"y" or "N"/"n" and decides who goes first
        turn = ((input("Do you want to go first (enter Y or N): ")).upper()).strip()
        if turn == "Y" or turn == "N":
            return turn
        else:
            print("Invalid Input.")
 
def place_ships(board_size):
    '''Places 3 user ships and 3 computer ships on the board.
 Takes in the parameter board size.
 Will place the ships randomly on the board for both the user and the computer.
 Returns a tuple (user_ships, computer_ships) in a dictionary.'''
    
    user_ships = {}
    computer_ships = {}
    #Sets up the dictionaries to place the ship positions in

    for i in range(3): #Loops for 3 user ships
        row = random.randrange(board_size) #Finds a random row to put the ship on
        col = random.randrange(board_size) #Finds a random column to put the ship on
        position = (row,col)
        #Finds a random position in the board for the user ship
    
        if position not in user_ships.values():
            ship_id = "user_ship_"+str(i)
            user_ships[ship_id] = position
    #Sets it as a ship position in the user_ships dictionary if it is not already in it

    while len(computer_ships)<3: #Loops for 3 computer ships
        row = random.randrange(board_size) #Finds a random row to put the ship on
        col = random.randrange(board_size) #Finds a random column to put the ship on
        position = (row,col)
        #Finds a random position on the board for the computer ship

        if (position not in user_ships.values()) and (position not in computer_ships.values()):
            ship_id = "computer_ship_"+str(len(computer_ships)+1)
            computer_ships[ship_id] = position
        #Sets it as a ship position in the computer_ships dictionary if it is not already in it
    
    return user_ships, computer_ships
    #Returns the user_ships and computer_ships dictionaries

def effects_of_mine(hit, affected_areas, rows, cols, board, computer_ships, user_ships):
   '''This function plays out certain tasks if a mine was hit. Takes in parameters
 hit (tuple), affected_areas (dictionary), rows (int), cols (int), board (2D list),
 computer_ships (dictionary), and user_ships (dictionary).
 Updates the board and removes any affected ships from dictionaries.
 Returns True if a mine exploded, otherwise False (bool).'''
   
   if hit in affected_areas.keys():
        print("\nA mine was hit!")
        ship_to_delete = ""
        board[rows][cols] = "*"
        affected = affected_areas[hit]
        del affected_areas[hit]
        #Demonstrates what areas were affected when the mine blasts
        for (a_row,a_col) in affected:
            if ((a_row,a_col) in computer_ships.values()):
                print("\nThe mine hit the computer's ship")
                board[a_row][a_col] = "X" #marks nearby ships with X
                for ships in computer_ships.keys():
                    if computer_ships[ships] == (a_row,a_col):
                        ship_to_delete = ships
                        break
                if ship_to_delete != "":
                    del computer_ships[ships] #deletes ships because they were blasted
                  
            elif ((a_row,a_col) in user_ships.values()):
                print("\nThe mine hit the user's ship")
                board[a_row][a_col] = "X" #marks nearby ships with X
                for ships in user_ships.keys():
                    if user_ships[ships] == (a_row,a_col):
                        ship_to_delete = ships
                        break
                if ship_to_delete != "":
                    del user_ships[ships] #deletes ships because they were blasted
                  
            else:
                board[a_row][a_col] = "*" #shown when mine did not hit ship
        
        #Is completed in case some mines are in the affected areas
        for (a_row, a_col) in affected:
           if (a_row,a_col) in affected_areas:
               effects_of_mine((a_row, a_col), affected_areas, rows, cols, board, computer_ships, user_ships)
        
        return True
   return False

def make_user_move(board, board_size,computer_ships, affected_areas, user_ships):
    '''
 Handles the user's missile input and updates the board accordingly.
 Takes in parameters board (2D list), board_size (int), computer_ships (dictionary),
 affected_areas (dictionary), and user_ships (dictionary).
 Updates the board and ship dictionaries depending on hit or miss.
 Returns nothing (None).
 '''
    
    valid_move = False #Used so that the question is asked over and over until the input is valid
    
    while not valid_move:
        try:
            row = int(input("Enter the row where you would like to enter your missile: "))
            col = int(input("Enter the column where you would like to enter your missile: "))
            #Asks for the user input for the coordinates of the missile
            rows = row-1
            cols = col-1
            hit = (rows,cols) #Stores the shot coordinates
            if ((0<=(rows)<board_size) and (0<=(cols)<board_size)) and board[rows][cols] == " ":
                #Checks if the shot is a mine
                if effects_of_mine(hit, affected_areas, rows, cols, board, computer_ships, user_ships):
                    valid_move = True
                
                elif hit in computer_ships.values(): #Checks if the shot was a hit
                    print("\nYou hit one of the computer's ships!")
                    board[rows][cols] = "X" #Marks the board and shows the user that it hit a ship
                    for key in computer_ships.keys():
                        if computer_ships[key] == hit:
                            del computer_ships[key] #Removes the destroyed ship from the board
                            break
                    valid_move = True
                
                else:
                    print("\nYou missed!")
                    board[rows][cols] = "O" #The shot did not hit
                    valid_move = True
            
            else:
                print("\nInvalid input. Please enter a position within the range or enter an empty cell.") 
                #Lets the user know that the input was invalid because the input was outside of the range
        
        except ValueError:
            print("Invalid Input. Please enter an integer.") 
            #Lets the user know that the input was invalid because a non-integer input was entered

def make_computer_move(board, board_size, user_ships, affected_areas, computer_ships):
    '''
    Randomly generates where the computer's missiles will fall and updates the board.
    Takes in parameters board (2D list), board_size (int), user_ships (dictionary),
    affected_areas (dictionary), and computer_ships (dictionary).
    Updates the board and ship dictionaries depending on hit or miss.
    Returns nothing (None).
    '''
    
    while True:
        rows = random.randrange(board_size)
        cols = random.randrange(board_size)
        hit = (rows,cols)
        #Finds a random coordinate to fire the missile

        if board[rows][cols] == ' ' or board[rows][cols] == "U": #Makes sure that the spot is valid
            #Checks if the shot is a mine
            if effects_of_mine(hit, affected_areas, rows, cols, board, computer_ships, user_ships):
                break
            
            elif hit in user_ships.values(): #Checks if the shot was a hit
                print("\nThe computer hit one of your ships!")
                board[rows][cols] = "X" #Updates the board that a ship was hit
                for key in user_ships.keys():
                    if user_ships[key] == hit: #Makes the value hit
                        del user_ships[key] #Deletes the hit ship
                        break
                break
                
            else:
                print("\nThe computer missed!")
                board[rows][cols] = "O" #Marks the shot as a miss
                break
 
def validate_board_size(board_size):
    '''Validates the board size chosen by the user, makes sure it is within 6 and 10.
  Takes in parameter board_size (int).
 Returns True if valid, otherwise False (bool).
 '''
    
    if 6<=(board_size)<=10: #Makes sure that the dimensions are within 6 and 10 
        return True
    else:
        return False

def gameboard_squares(board_size):
    '''
 Creates the gameboard with empty spaces based on the board size that the user wants.
 Takes in the parameter board_size (int).
 Returns a well-designed 2d list that makes up the gameboard.
 '''
    
    rows, columns = board_size, board_size
    board = []
    
    for _ in range(rows):
        board.append([" "]*columns) #Fills every row with empty spaces
    
    return board

def display_board(board, user_ship):
    '''
 Displays the current state of the game board.
 Takes in parameters board (2D list) and user_ship (dictionary).
 Displays user ships with a "U" and marks hit/miss with "X"/"O".
 Returns nothing (None).
 '''
    
    print("  ", end=" ")
    for header in range(len(board[0])):
        print("  %2d " % (header+1), end="") #Prints the column numbers
    print()

    length = len(board)
    for row in range(length):
        row_str = "%2d |" % (row+1) #Creates the row numbers
        col_str = "   +"
        for col in range(length):
            ship = (row,col)
            if ship in user_ship.values() and board[row][col] == " ":
                board[row][col] = "U" #Shows the user ships to the user
            row_str += " %2s |" % board[row][col]
            col_str += "----+"
        print(col_str)
        print(row_str)
    print(col_str)

def winner(user_ships, computer_ships):
    '''
 Determines and prints the outcome of the game.
 Takes in parameters user_ships (dictionary) and computer_ships (dictionary).
 Compares lengths to decide winner or tie.
 Returns the winner as tie, computer, or user (all strings).
 '''
    
    if len(user_ships) == 0 and len(computer_ships) == 0: #If both sides lost all their ships at the same time
        print("\nT I E")
        return "tie"
    elif len(user_ships) == 0: #If the user lost all of their ships first
        print("\nT H E  C O M P U T E R  W O N!") 
        return "computer"
    elif len(computer_ships) == 0: #If the computer lost all of its ships first
        print("\nT H E  U S E R  W O N!")
        return "user"

def place_mines( user_ships, computer_ships, board_size):
    '''
 Randomly places 1 to 3 mines on the board avoiding ship positions.
 Takes in parameters user_ships (dictionary), computer_ships (dictionary), and board_size (int).
 Randomly selects mine positions and assigns blast types.
 Returns a dictionary of mine positions and their types.
 '''
    
    number_of_mines = random.randint(1,3)
    mines = {}
    
    while len(mines)<number_of_mines:
        row = random.randrange(1,board_size-1) #Chooses a random row to put the mine on
        col = random.randrange(1,board_size-1) #Chooses a random column to put the mine on
        mine = (row,col)
        if (mine not in user_ships.values()) and (mine not in computer_ships.values()):
            mine_type = random.randint(1,2) # 1 for a larger blast, 2 for a smaller blast
            mines[mine] = mine_type
    
    return mines

def mine_damage(mines):
    '''
 Calculates the affected area for each mine on the board.
 Takes in parameter mines (dictionary).
 Determines surrounding tiles based on mine type (1 or 2).
 Returns a dictionary of mine positions mapped to affected positions (dictionary).
 '''
    
    affected_area = {} #Creates a dictionary and stores values for the affected area
    
    for key in mines:
    #Finds the row and column of the current mine
        row = key[0]
        col = key[1]
        mine_type = mines[key]
        
        if mine_type == 1:
            affected_areas = [(row+1, col-1), (row+1,col), (row+1, col+1),
                (row, col-1), (row, col+1), (row-1, col-1),
                (row-1, col), (row-1,col+1)]
            #Finds the affected area of the mine if it is a big one
            mine = (row,col)
            affected_area[mine] = affected_areas
        
        else:
            affected_areas = [(row+1, col), (row, col-1), 
                (row, col+1),(row-1, col)]
            #Finds the affected area of the mine if it is in the shape of a cross
            mine = (row,col)
            affected_area[mine] = affected_areas
    
    return affected_area

def welcome_message():
    """
 Displays the welcome message and rules of the game.
 Takes no parameters.
 Prints game instructions and objectives.
 Returns nothing (None).
 """
    
    print("W E L C O M E  T O  B A T T L E S H I P:")
    #Instructions for the user
    print("\nThe rules are simple! Each player (you and the computer) has 3 ships.", 
        "Your goal is to hit the opponents ships. The first one to hit all the ships wins!", 
        "Note, that the ships you will observe when the board is ready (the ones labelled U)", 
        "belong to YOU! So do not try to bomb them!", 
        "Also, hidden around the board are secret mines! These mines can sink your opponents ship,", 
        "but they can also hit you!")
    print("\nNow that's all for the instructions! It's finally time for the fun part: start playing!\n")

def game(turn, user_ships, computer_ships, board, board_size, affected_areas):
    """
 Manages the game by using functions to allow players to take turns and calls the appropriate functions.
 Takes in parameters turn (str), user_ships (dictionary), computer_ships (dictionary),
 board (2D list), board_size (int), and affected_areas (dictionary).
 Handles game flow until a win/loss/tie condition is met.
 Returns nothing (None).
 """
    
    #Allows players to take turns and play the game
    while ((len(user_ships))>0) and ((len(computer_ships))>0):
        if turn == "Y":
            print("\nNow it is your turn!\n")
            make_user_move(board, board_size,computer_ships, affected_areas, user_ships)
            display_board(board, user_ships)
            turn = "N" 
        elif turn == "N":
            make_computer_move(board, board_size,user_ships, affected_areas,computer_ships)
            print("\nThis was the computer's move.")
            display_board(board, user_ships)
            turn = "Y"

def get_board_information():
    """This function gets all the information
 needed to make the game's gameboard and returns board and board_size"""
    
    #Asks the user for the board size they want
    while True:
        board_size = int(input("Enter a value between (6 to 10) to initalize the board size: "))
        if validate_board_size(board_size):
            board = gameboard_squares(board_size) #Generates the gameboard
            break
        else:
            print("Invalid input. Try Again") #Tells the user that their input is invalid
    return board, board_size

def display_computer_surviving_ships(board, computer_ships):
   """
   This function allows the game to display where the computer's ships
   were located if the computer won the game. Takes in board (2D list) and
   computer_ships (dictionary). Returns nothing (None).
   """

   for (row, col) in computer_ships.values():
      board[row][col] = "C" #Shows the "C" on the board

def message_if_computer_wins(result, board, computer_ships, user_ships):
    """"
    This function allows the program to print out the additional information
    (such as the remaining computer ships) in the case that the computer has won.
    It takes in result (string), board (2D list), computer_ships (dictionary),
    and user_ships(dictionary). Returns nothing (None).
    """

    #Calls all needed functions to display the computer's remaining ships
    if result == "computer":
        display_computer_surviving_ships(board, computer_ships)
        print("\n The squares with the letter 'C' are the computer's ships that still managed to survive!\n")
        display_board(board,user_ships)

def main():
    '''Mainline Logic.'''
    welcome_message() #displays instructions + welcome message

    #gets board information and related values
    board, board_size = get_board_information()
    #Randomly places the user's and computer's ships somewhere on the board
    user_ships, computer_ships = place_ships(board_size)
    #Places mines on the board, making sure that the ships and mines do not overlap
    mines = place_mines(user_ships, computer_ships, board_size)
    #Determines the affected areas from the mines
    affected_areas = mine_damage(mines)

    display_board(board,user_ships)  #Displays the board

    #Asks the user if they want to go first
    turn = validate_first()
    game(turn, user_ships, computer_ships, board, board_size, affected_areas) #Begins game
    result = winner(user_ships, computer_ships) #Displays winner
    #Only displayed if the computer wins
    message_if_computer_wins(result, board, computer_ships, user_ships)

main()
#By: Lukas Trisauskas
#Course: Computer Science, Year 1

import random
import time
# Main function that encapsulates all classes and methods
# It is used to call the function whenever the player wants to restart the game
def main():
        
    # Parent class
    class Player:
        
        # Initializer 
        # Initiate a class instance
        def __init__(self, name, marker):
            self.name = name
            self.marker = marker
            
        # __str__ returns instance of object as string
        def __str__(self):
            return self.marker, self.name
        
    # Child class, inherits attributes of parent class (Player)
    class Human(Player):
        
        # Retrieves the position from the Human player.
        def get_position(self):
            position = int(input(f"Please enter a position from 1 to 9: "))
            return position
        
    # Child class, inherits attributes of parent class (Player)
    class Computer(Player):
        # Generates a random position based on what positions there are left on the board
        def random_move(self, board):
            empty = []
            for i in range(len(board)):
                if board[i] == " ":
                    empty.append(i+1)
            move = random.choice(empty)
            empty.remove(move)
            return move
            
    def board_state(board, patterns):
        state = []
        for pattern in patterns:
            temporary = []
            state.append(temporary)
            for element in pattern:
                for corresponding in board[element-1]:
                    temporary.append(corresponding) 
        return state

    # Looks for a match based on the current board_state
    # Counts how many markers there are for both players
    # Comapres the count of markers to the lenght of each pattern list
    def match_marker():
        current_state = board_state(board, patterns)
        for marker in current_state:
            count_player_1 = marker.count(player_1.marker)
            count_player_2 = marker.count(player_2.marker)
            
            if count_player_1 == len(marker): return player_1
            if count_player_2 == len(marker): return player_2
            
    # This prints a board representation on the screen
    def print_board(board):
        board = f"""
            {board[0]} | {board[1]} | {board[2]}
            ---------
            {board[3]} | {board[4]} | {board[5]}
            ---------
            {board[6]} | {board[7]} | {board[8]}
        """
        print(board)

    # Checks if the position has been take either by you or oponent
    def position_taken(board, position):
        index = board[position-1]
        if index == " ": return False
        elif index != current_player or index != " ": return True
        
        
    # Checks if there are empty strings in board
    # Used to check if the game is a tie
    def empty_board(board):
        if ' ' in board: return True
        else: return False

    # Assigns the current_player marker to the position (board index) they entered
    # And calls print_board() to print the updated board
    # Takes three arguments, board list, the position and marker of current_player
    def update_board(board, position, marker):
        board[position-1] = marker
        print_board(board)
        return board

    # Changes player turns, gets called everytime current_player makes a move
    def change_turns(current_player):
        if current_player == player_1: next_player = player_2
        if current_player == player_2: next_player = player_1
        return next_player

    # Picks a random player at the start of the game and assigns it to current_player
    def first_player(player_1, player_2):
        first_player = random.choice([player_1, player_2])
        return first_player

    # A menu which allows you to choose between different game modes.
    # Creates instance of Player class based on the mode the user picks
    def select_game_mode():
        commands = """
        Mode | Command
        --------------
        PvP  |   1
        --------------
        PvC  |   2
        --------------
        CvC  |   3
        """
        while True:
            print(commands)
            try:
                mode = int(input("Select the mode you would like to play: "))
                if mode == 1:
                    # Creates an instance of Human class and is assigned to player_1 and player_2
                    player_1 = Human("Player 1", "X")
                    player_2 = Human("Player 2", "O")
                    # Returns the mode, player_1 and player_2 object (class instance)
                    return 'PvP', player_1, player_2
                elif mode == 2:
                    player_1 = Human("Player 1", "X")
                    player_2 = Computer("Computer", "O")
                    return 'PvC', player_1, player_2
                elif mode == 3:
                    player_1 = Computer("Computer 1", "X")
                    player_2 = Computer("Computer 2", "O")
                    return 'CvC', player_1, player_2
            except ValueError:
                print("To continue please select one of the modes")

    # This is the main function of the game
    def start(board, current_player, mode):
        match_found = False
        board_full  = False
        while True:
            print_board(board)
            print(f"Current player: {current_player.name}")
            match = match_marker()
            if match == player_1 or match == player_2:
                print(f"{match.name} wins.")
                match_found = True
                break
            elif not empty_board(board):
                print("The game is a tie.")
                board_full = True
                break
            # checks if the instance of current_player is part of Computer class and that the mode is PvC
            elif isinstance(current_player, Computer) and mode == "PvC":
                
                # Retrieves the random position from Computer
                # Passed onto update_board, including the current_player.marker
                # Updates and print the board
                # Changes turns by assigning the current_player to function change_turns
                # Takes argument current_player
                position = current_player.random_move(board)
                update_board(board, position, current_player.marker)
                print(f"{current_player.name} selects position: {position}")
                current_player = change_turns(current_player)
                
                # Not part of the assessment
                # Computer vs Computer
                # This will run only if the current_player is instance of Computer class and the mode is CvC
            elif isinstance(current_player, Computer) and mode == "CvC":
                position = current_player.random_move(board)
                update_board(board, position, current_player.marker)
                print(f"{current_player.name} selects position: {position}")
                current_player = change_turns(current_player)
                time.sleep(1)
            # checks if the instance of current_player is part of Human class and if the mode is PvP or PvC
            # This means that human player will be able to play both modes
            elif isinstance(current_player, Human) and mode == "PvP" or mode == "PvC":
                try:
                    position = current_player.get_position()
                    if position not in range(1, 10):
                        print(f"Position {position} not in range!")
                    elif position in range(1,10) and position_taken(board, position) == False:
                        update_board(board, position, current_player.marker)
                        print(f"{current_player.name} moves to position {position}")
                        current_player = change_turns(current_player)
                    elif position_taken(board, position) == True:
                        print(f"Position {position} is occupied")
                except ValueError:
                    print("Please select a postion to continue!")
        if match_found or board_full:
            while True:
                try:
                    restart = input("Would you like to play again? (y/n): ")
                    if restart in ["Y", "y"]:
                        main()
                    elif restart in ["N", "n"]:
                        print()
                        print("Thank you for playing.")
                        exit()
                    else:
                        raise ValueError
                except ValueError:
                    print("To continue plese enter y or n.")
            
    board = [" ", " ", " ", " ", " ", " ", " ", " ", " ",]
    patterns = [
            [1,2,3],[4,5,6],[7,8,9], # horizontal pattern
            [1,4,7],[2,5,8],[3,6,9], # vertical pattern
            [1,5,9],[3,5,7]]         # diagonal pattern

    mode, player_1, player_2 = select_game_mode()
    # Here I call the first_player function, which picks a random player and assigns it to current_player
    current_player = first_player(player_1, player_2)
    # This starts the game, we pass the board, current_player and mode to the function
    start(board, current_player, mode)

main()
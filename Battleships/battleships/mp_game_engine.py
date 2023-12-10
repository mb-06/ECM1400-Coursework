import random
from components import initialise_board,create_battleships,place_battleships
from game_engine import attack, cli_coordinates_input 
import logging
players = {}


def generate_attack(board:list[list], attacked_points:list)->tuple:
    ''''
    Generates coordinates for a random attack on a given board

    Args:
    board : A list of lists representing the board that can be attacked
    attacked_points : A list with points that have already been attacked
    
    Returns :  
    attack_coords : A tuple representing a coordinate to be attacked
    '''
    if type(board) != list or type(attacked_points) != list:
            raise TypeError('Board and attacked points needs to be lists')
    logging.info('Generating attack')
    size = len(board)
    new_point = False #Allows checking if it is a new point
    while new_point == False:
        row_attack = random.choice(range(size)) #Gets random point
        column_attack = random.choice(range(size))
        attack_coords = (column_attack,row_attack)
        if attack_coords in attacked_points: #Checks if point is in list of previous guesses
            logging.info('Point already been generated, generating new point')
            continue
        else:
            attacked_points.append(attack_coords) #Adds to previous guesses
            new_point = True
    logging.info('Attack generated')
    return attack_coords

def ai_opponent_game_loop():
    '''
    Runs a game of battleships against an AI opponent
    '''
    logging.info('##### ai opponent game loop started #####') #Hashes used to highlight start of new game
    print('Welcome to the game! Sink all battleships to win\nEnter coordinates (0-9) to guess\nYour board will be displayed where: \nA letter represents a ship\n- represents an empty space not attacked\n* represents an AI missed attack\nX represents an AI hit\nPress q at anytime to quit') #Starts game with welcome message
    try:
        start_quest = 1
        while start_quest != 0:
            start_quest = int(input('\n\nPress 0 to start')) #Allows user to read before starting
        correct_difficulty = False
        while correct_difficulty == False:
            diff = int(input('Select difficulty:\n 0 - Very Easy\n 1 - Slighlty less easy'))
            if diff in [0,1]:
                correct_difficulty = True
    except:
        raise ValueError('Please enter an integer when requested')
    empty_board_user = initialise_board() #Initialises board for user
    empty_board_AI = initialise_board() #Initialises a seperate board for AI
    battleships_user = create_battleships() #Create two seperate dictionaries for AI and user 
    battleships_AI = create_battleships()
    user_board = place_battleships(empty_board_user,battleships_user,'custom') #Places user ships using custom json
    if diff == 0:
        logging.info('Very Easy chosen')
        AI_board = place_battleships(empty_board_AI,battleships_AI,'random') #Places AI ships randomly
    elif diff == 1:
        logging.info('Slightly less easy chosen')
        AI_board = place_battleships(empty_board_AI,battleships_AI,'optimised') #Places AI with optimised algorithm
    players['User'] = [user_board,battleships_user] #Assigns user the user board
    players['AI'] = [AI_board,battleships_AI] #Assigns AI the AI board
    user_attack_list = [] #Used to stop repeated guesses by user
    AI_attack_list =[] #Used to stop repeated guesses by AI
    board_asci = initialise_board() #Creates empty board for ASCII 
    board_asci_length = len(board_asci) 
    for row in range(board_asci_length): #Goes through every point
        for column in range(board_asci_length):
            if user_board[row][column] == None:
                board_asci[row][column] = '-' #If empty use -
            else: #If there is a ship, use the first letter
                board_asci[row][column] = str(user_board[row][column][0])
    logging.info('ASCII board created')
    print('Current User Board:')
    for line in board_asci: #Displays the current board
        print('   '.join(line)) #Uses .join to display without brakcets
    user_is_out = all(value == 0 for value in players['User'][1].values()) #Checks if all ships are sunk
    AI_is_out = all(value == 0 for value in players['AI'][1].values())
    while user_is_out == False and AI_is_out ==False:
        coords_good = False 
        while coords_good == False: #Whilst the point isnt valid
            user_attack = cli_coordinates_input() #Asks for point
            if user_attack == None: #Allows user to quit
                logging.info('Game has been quit')
                print('Game has been quit')
                quit()
            elif user_attack == False: #Allows repeating on invalid inputs
                logging.error('Integers not entered')
                print('Please enter integers')
                continue
            elif user_attack[0]>len(AI_board)-1 or user_attack[1]>len(AI_board)-1: #Checks if it fits in the board
                logging.error('Coordinate does not fit in the board')
                print('Invalid, try again')
            elif user_attack in user_attack_list: #Checks it is original
                logging.error('Coordinate already attacked')
                print('Already attacked, try again')
            else:
                user_attack_list.append(user_attack) #Adds to list to check originality
                coords_good=True
        attack_result_user = attack(user_attack,AI_board,battleships_AI) #Attacks the AI board
        if attack_result_user == True:
            logging.info('User has hit AI at %s', user_attack)
            print(' User : Hit')
        else:
            logging.info('User has missed AI at %s', user_attack)
            print('User : Miss')
        AI_attack = generate_attack(user_board,AI_attack_list) #generates AI attack(randomly), updates list of attacks
        attack_result_AI = attack(AI_attack,user_board,battleships_user) #AI attacks user board
        if attack_result_AI ==True:
            logging.info('AI has hit User at %s',AI_attack)
            board_asci[AI_attack[1]][AI_attack[0]] = 'X'
            print('AI : Hit')
            print('Current User Board:')
            for line in board_asci: #Displays the current board
                print('   '.join(line))
        else:
            logging.info('AI has missed User at %s',AI_attack)
            board_asci[AI_attack[1]][AI_attack[0]] = '*'
            print('AI : Miss')
            print('Current User Board:')
            for line in board_asci: #Displays the current board
                print('   '.join(line))
        user_is_out = all(value == 0 for value in players['User'][1].values()) #Checks if all ships are sunk
        AI_is_out = all(value == 0 for value in players['AI'][1].values())
    if user_is_out == True: #Checks who wins
        logging.info('AI has won the game')
        print('AI has won')
    else:
        logging.info('User has won the game')
        print('User has won')

if __name__ == '__main__':
    logging.basicConfig(filename = 'mp_game_engine.log',level = logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ai_opponent_game_loop()


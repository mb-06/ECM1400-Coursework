from components import initialise_board,create_battleships,place_battleships
import logging

#Note: In components, we used format(y,x), however here we use (x,y) to make it compatible to main.py

def attack(coordinates:tuple,board:list[list],battleships:dict)->bool:
    '''
    Will process an attack, saying if it hits a ship or not and updating
    the ship sizes accordingly

    Args:
    coordinates : A tuple with the row and column in form (x,y)
    board : list of lists representing the current board
    battleships : dictionary with key of ship name and value of ship size

    Returns:
    result : boolean. True means hit, False means miss.
    '''
    try:   
        if len(coordinates) == 2: #Checks if tuple is correct size
            y_attack = int(coordinates[1]) #Gets y coordinate
            x_attack = int(coordinates[0]) #gets x cooridnate
            coordinate_attack = board[y_attack][x_attack] #Gets attack
            if coordinate_attack == None:
                return False #If the space is empty, False retuned
            else: #If space isn't empty
                battleships[coordinate_attack] = battleships[coordinate_attack] -1 #Updates dictionary
                board[y_attack][x_attack] = None #Sets it to None, updating the board
                return True
        else:
            logging.error('Coordinates not in correct format')
            raise ValueError('Coordinates need to be in form (y,x)') #If tuple not correct size, raises an error
    except TypeError: #This will catch all errors in the structures of the arguments 
        logging.error('Error in the type of  the arguments')
        raise TypeError('Error in one of the arguments, check docstring')

def cli_coordinates_input()->tuple:
    '''
    Produces a tuple based on user inputted row and column values

    Returns:
    coordinate : tuple with first value indicating row inputted and second value indicating column inputted
                 returns False if a string is entered, and None if q is entered
    '''
    coordinate = False #Response if not an integer and not quit
    y_coord = input('What row to attack :')
    x_coord = input('What column to attack :')
    if y_coord == 'q' or x_coord == 'q': #Allows user to quit in the game(doesn't effect functionality required)
        logging.info('q has been entered')
        coordinate = None
    elif y_coord.isnumeric() and x_coord.isnumeric(): #Checks if there are integers
            logging.info('Two integers have been entered')
            coordinate = (int(x_coord),int(y_coord)) #Int() here in the try except to allow invaliud inputs to promote another input
    else:
        logging.error('Non integers have been entered')
    return coordinate

def simple_game_loop():
    '''
    Runs a simple game of battleships, prompting the user to attack a simply generated board
    '''
    logging.info('##### Simple game loop started #####')
    print('Welcome to the game\nPress q to quit at any time') #Welcome message
    initialised_board = initialise_board() #Initialises empty board
    battleships = create_battleships()  #Gets the dictionary for the ships
    placed = place_battleships(initialised_board,battleships) #Places the ships using default 'simple' argument
    attacked_coords = [] #Sets up to track guesses
    size_board = len(placed) #Used to tell user what numbers to input
    while all(value == 0 for value in battleships.values())==False: #this is saying whilst the dictionary still has at least one ship with a non zero left in the dictionary
        coord_good = False #Sets variable to be used to make sure the coordinate is good
        while coord_good == False: # Allows incorrect inputs, we ask for them again
            attack_coordinates = cli_coordinates_input() #Asking for a coordinate
            if attack_coordinates == None: #Allows user to quite by entering 'q' see cli_coordinates_input()
                print('Game has been quit')
                logging.info('Game has been quit')
                quit()
            elif attack_coordinates == False: #Allows strings entered to be retried
                print('Please enter integers')
                logging.error('Integers have not been entered') #Uses .error to signify erroneous input
                continue 
            if attack_coordinates[0]>len(placed)-1 or attack_coordinates[1]>len(placed)-1: #Checks if the coordinate fits in the board or not
                print(f'Point not in the game board, enter a values from 0 to {size_board}')
                logging.error('Coordinates do not fit the playing board')
                continue
            if attack_coordinates in attacked_coords: #Stops users not inputting the same point again
                print('This point has already been attacked, try again')
                logging.error('Coordinates have already been attacked')
                continue
            else:
                coord_good=True #Stops the loop. Allows the attack to now be processed
                attacked_coords.append(attack_coordinates) #Keeps a log of all user attacks
        attack_result = attack(attack_coordinates,placed,battleships) #Processes the attack
        if attack_result ==True: #Shows the result of the attack
            logging.info('Player hit at %s', attack_coordinates)
            print('Hit') 
        else:
            logging.info('Player missed at %s', attack_coordinates)
            print('Miss')  
    logging.info('Game has ended')     
    print('All ships have been sunk, the game is over') #When all values of dictioanry are zero, we end the game with this message

    
if __name__ == '__main__':
    logging.basicConfig(filename = 'game_engine.log',level = logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    simple_game_loop()

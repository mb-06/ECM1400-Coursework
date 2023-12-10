import random
import json
import logging


def initialise_board(size:int=10 )->list[list]:
    '''
    Initialises a n by n board of None values, 
    where n is the size
    
    Args:
    size : Size of the board (both dimensions), default size of 10.
    
    Returns:
    empty_board : List with n lists each with n inputs of None, whre n=size
    '''
    try:
        empty_board = [[None]*size for x in range(size) ] #List comprehension gets None n times as list a makes a list of n of these lists
        logging.info('Empty board has been created')
    except TypeError: #Raises exception when integer not inputted
        logging.error('Input to initialise_board() is not an integer') #Error log, work out
        raise TypeError('Need an integer input')
    return empty_board


def create_battleships(filename:str='battleships.txt')->dict:
    '''
    Creates a dictionary for the size of the ships from 
    provided text file.

    Args:
    filename : file to be read with ship information of format ship_name:size,
                default of battleships.txt

    Returns:
    ships_dict : Dictionary with ship types as keys and their sizes as values
    '''
    try:
        ships_dict = {} #Creates an empty dictionary    
        with open(filename,'r') as ships:
            for item in ships: #Iterates through each input in the text file
                ship_name = item.split(':')[0] #Due to structure of the text file, split by :
                ship_size = int(item.split(':')[1])
                if ship_name not in ships_dict:
                    ships_dict[ship_name] = ship_size #Enters name and relevant size
                else: #Checks if ship is already in the dictionary
                    logging.error('Text file has repeated ship names')
                    raise ValueError('Text file has repeated ship names')
        logging.info('Ship dictionary created')
    except TypeError: #Raises exception if not a text file
        logging.error('.txt file not inputted') #Error log
        raise TypeError('Need a .txt file input')
    except IndexError: #Here will regard incorrectly formatted text files, where colon isn't used
        logging.error('')
        raise IndexError('File needs to be in format ship_name:size')
    except ValueError: #Here again regards incorrectly formatted text files, where integers not used
        raise ValueError('Size needs to be an integer in the .txt file')
    return ships_dict


def place_battleships(board:list[list], ships:dict,placement:str='simple',custom_json = 'placement.json')->list[list]:
    ''' 
    Creates a board with ships placed based on algorithm wanted

    Args:
    board : a list of list with none values 
    ships : dictionary with key of ship name and value of ship size
    placement : string indicating what algorithm of placement to use, default of 'simple'
        Can take values 'simple','random','custom'
    custom_json : string to indicate the use of a json file for the custom placement, default of 'placement.json'

    Returns:
    board : the original board now with ships placed 
    '''
    try:
        summed_sizes = sum(ships.values()) #Sums how many boxes will be used by the ships
        board_size = len(board)
        if summed_sizes> board_size**2: #If ships take up more space than available, raise an error
            logging.error('Board size not big enough for ship sizes')
            raise TypeError('Board size not big enough for ship sizes')
    except AttributeError:
        raise AttributeError('ships is not a dictionary')
    try:
        if placement.lower() == 'simple':
            logging.info('Simple algorithm chosen')
            ship_number = 0 #Starts in the first row
            for ship_name,size  in ships.items():
                for index in range(size): #Starting from first column, then goes value amount across
                    board[ship_number][index] = ship_name #Sets the input to the name of the ship
                ship_number +=1 #Goes to the next row for the new ship
            logging.info('Simple algorithm complete')
        elif placement.lower() == 'random':
            logging.info('Random algorithm chosen')
            board_length = len(board)
            for ship_name,size  in ships.items():
                which_way = random.choice(['h','v']) #Randomly choses for the ship to be vertical or horizontal
                logging.info('direction chose %s',which_way)
                check =False #Check is to see if the ship has been placed
                while check == False: 
                    if which_way == 'h':
                        starting_point_x = random.choice(range(board_length-size+1)) #Choses a random x value for which the ship can fit
                        starting_point_y = random.choice(range(board_length)) #Choses a random y value
                        logging.info('Random point is %s', (starting_point_y,starting_point_x))
                        count = 0
                        for i in range(size): #This loop checks if all values are None (ie: No ships there already)
                            if  board[starting_point_y][starting_point_x+i] == None:
                                count += 1
                        if count == size: #We then input the ship if no ships are there already, or repeats the loop
                            for i in range(size):
                                board[starting_point_y][starting_point_x+i] = ship_name
                            check = True #Stops while loop, moving to the next ship
                        else:
                            logging.info('Ships does not fit at starting point %s direction %s',(starting_point_y,starting_point_x),which_way)
                            continue

                    if which_way == 'v':
                        starting_point_y = random.choice(range(board_length-size+1)) #Choses a random y value for which the ship can fit
                        starting_point_x = random.choice(range(board_length)) #Choses a random x value
                        logging.info('Random point is %s', (starting_point_y,starting_point_x))
                        count = 0
                        for i in range(size): #This loop checks if all values are None (ie: No ships there already)
                                if board[starting_point_y+i][starting_point_x] == None:
                                    count +=1
                        if count == size: #We then input the ship if no ships are there already, or repeats the loop
                            for i in range(size):
                                board[starting_point_y+i][starting_point_x] = ship_name
                            check =True #Stops while loop, moving to the next ship
                        else:
                            logging.info('Ships does not fit at starting point %s direction %s',(starting_point_y,starting_point_x),which_way)
                            continue
                logging.info('Random algorithm complete')
        elif placement.lower() == 'custom':
            logging.info('Custom algorithm chosen')
            try: #Try, except used to make sure input is valid json file
                if type(custom_json)==str:  #Checks if it is a json file, then loads it
                    file = open(custom_json)
                    place_json = json.load(file) 
                else:
                    place_json = custom_json #If already a json file, uses it as it is
                for ship_name in place_json: 
                    size = ships[ship_name] #Gets the size of the set ship
                    starting_point_x = int(place_json[ship_name][0]) #Gets the starting x
                    starting_point_y = int(place_json[ship_name][1]) #Gets the starting y
                    if place_json[ship_name][2] == 'h': #Checking which direction it is supposed to be 
                        count = 0 
                        for i in range(size):
                            if board[starting_point_y][starting_point_x+i] == None: #Checks if space is empty
                                count+=1
                        if count == size: #If the space is empty, input the ship
                            for i in range(size):
                                board[starting_point_y][starting_point_x+i] = ship_name
                        else: #This is used in case the json file has overlapping ships
                            logging.error('JSON file has overlapping ships')
                            raise ValueError('Invalid Inputs, does not fit')
                    
                    if place_json[ship_name][2] == 'v': #Repeats for vertical ships
                        count = 0 
                        for i in range(size):
                            if board[starting_point_y+i][starting_point_x] == None:
                                count+=1
                        if count == size:
                            for i in range(size):
                                board[starting_point_y+i][starting_point_x] = ship_name
                        else:
                            logging.error('JSON file has overlapping ships')
                            raise ValueError('Invalid Inputs, does not fit')
                logging.info('Custom algorithm complete')
   
            except TypeError: #If a Json file not used, it will raise a TypeError
                logging.error('Incorrect file type used')
                raise TypeError('Enter a valid json file, with inputs related to board size')    

        elif placement.lower() == 'optimised':
            logging.info('optimised algorithm chosen')
            board_length = len(board)
            for ship_name,size  in ships.items():
                which_way = random.choices(['h','v'],weights = [0.3,0.7],k=1)[0] #Here we make it more likely for vertical, as these are less likely to be guessed
                logging.info('direction chose %s',which_way)
                check =False #Check is to see if the ship has been placed
                while check == False: 
                    if which_way == 'h':
                        #Want smaller boats to be near the edges with higher probability
                        if size < 3:
                            initial_prob = [2/board_size] #Set start and end probabilities to be higher
                            end_prob = [2/board_size]
                            middle_probs = [(board_size-4)/((board_size)*(board_size-2)) for i in range(board_size-2)] #Set the rest of the probabilities, that are less
                            for i in range(len(middle_probs)):
                                initial_prob.append(middle_probs[i])
                            initial_prob.append(end_prob[0]) #Now all probabilities are in one list
                            starting_point_x = random.choice(range(board_length-size+1)) #Choses a random x value for which the ship can fit
                            starting_point_y = random.choices(range(board_length),weights = initial_prob,k=1)[0] #Choses a random y value
                        
                        else:
                            starting_point_x = random.choice(range(board_length-size+1)) #Choses a random x value for which the ship can fit
                            starting_point_y = random.choice(range(board_length)) #Choses a random y value                     
                        logging.info('Random point is %s', (starting_point_y,starting_point_x))
                        count = 0
                        for i in range(size): #This loop checks if all values are None (ie: No ships there already)
                            if  board[starting_point_y][starting_point_x+i] == None:
                                count += 1
                        check_alone = True
                        if count == size: #We then input the ship if no ships are there already, or repeats the loop
                            #Here we check if boats are next to eachother
                            if starting_point_y != 0 :  #Checks if above points are empty
                                for i in range(size):
                                    if board[starting_point_y-1][starting_point_x+i] != None:
                                        check_alone = False
                                        #break
                            if starting_point_y != board_size - 1: #Checks if below points are empty
                                for i in range(size):
                                    if board[starting_point_y+1][starting_point_x+i] != None:
                                        check_alone = False
                                            #break
                            if starting_point_x != 0: #Checks if space before is empty
                                if board[starting_point_y][starting_point_x-1] != None:
                                    check_alone = False
                                    #break
                            if starting_point_x + size != board_size: #Checks if space after is empty
                                if board[starting_point_y][starting_point_x+size] != None:
                                    check_alone = False
                                   # break
                        if check_alone == True and count == size:    
                            for i in range(size):
                                board[starting_point_y][starting_point_x+i] = ship_name
                            check = True #Stops while loop, moving to the next ship
                        else:
                            logging.info('Ships does not fit at starting point %s direction %s',(starting_point_y,starting_point_x),which_way)
                            continue
                    if which_way == 'v':
                        #Want smaller boats to be near the edges with higher probability
                        if size < 3:
                            initial_prob = [2/board_size] #Set start and end probabilities to be higher
                            end_prob = [2/board_size]
                            middle_probs = [(board_size-4)/((board_size)*(board_size-2)) for i in range(board_size-2)] #Set the rest of the probabilities, that are less
                            for i in range(len(middle_probs)):
                                initial_prob.append(middle_probs[i])
                            initial_prob.append(end_prob[0])
                            starting_point_x = random.choices(range(board_length),weights= initial_prob,k=1)[0] #Choses a random x value for which the ship can fit
                            starting_point_y = random.choice(range(board_length-size+1)) #Choses a random y value
                        
                        else:
                            starting_point_x = random.choice(range(board_length)) #Choses a random x value for which the ship can fit
                            starting_point_y = random.choice(range(board_length-size+1)) #Choses a random y value
                        logging.info('Random point is %s', (starting_point_y,starting_point_x))
                        count = 0
                        for i in range(size): #This loop checks if all values are None (ie: No ships there already)
                            if  board[starting_point_y+i][starting_point_x] == None:
                                count += 1
                        check_alone = True
                        if count == size: #We then input the ship if no ships are there already, or repeats the loop
                            #Here we check if boats are next to eachother
                            if starting_point_x != 0: #Checks if above spaces are empty
                                for i in range(size):
                                    if board[starting_point_y+i][starting_point_x-1] != None:
                                        check_alone = False
                                        #break
                            if starting_point_x != board_size-1: #Checks if below spaces are empty
                                for i in range(size):
                                    if board[starting_point_y+i][starting_point_x+1] != None:
                                        check_alone = False
                                        #break
                            if starting_point_y != 0: #checks if space before is empty
                                if board[starting_point_y-1][starting_point_x] != None:
                                    check_alone = False
                                   # break
                            if starting_point_y + size != board_size: #checks if space after is empty
                                if board[starting_point_y+size][starting_point_x] != None:
                                    check_alone = False
                                    #break
                        if check_alone == True and count == size:    
                            for i in range(size):
                                board[starting_point_y+i][starting_point_x] = ship_name
                            check = True #Stops while loop, moving to the next ship

                        else:
                            logging.info('Ships does not fit at starting point %s direction %s',(starting_point_y,starting_point_x),which_way)
                            continue
                logging.info('optimised algorithm complete')
        else: #If invalid placement is used
            logging.error('Placement type invalid')
            raise ValueError('Incorrect placement input')
    except: #All other exceptions due to inputs
        logging.error('Incorrect arguments')
        raise TypeError('Type of input incorrect, refer to docstring')
    return board

if __name__ == '__main__':
    logging.basicConfig(filename = 'components.log',level = logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    # allows logging for individual module

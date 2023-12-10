from components import initialise_board,place_battleships,create_battleships
import pytest

import test_helper_functions as thf #Uses the given test_helper_functions module to provide a report
testReport_c = thf.TestReport("test_components_report.txt")

def test_initialise_board_correct_size():
    """
    Test if the initialise_board function returns a list of the correct size
    """
    size = 10
    board = initialise_board(size) # Run the function
    try:
        assert isinstance(board, list), "initialise_board function does not return a list"  # Check that the return is a list
        assert len(board) == size, "initialise_board function does not return a list of the correct size" # Check that the length of the list is the same as board
        for row in board:
            assert isinstance(row, list), "initialise_board function does not return a list of lists" # Check that each sub element is a list
            assert len(row) == size, "initialise_board function does not return lists of the correct size" # Check that each sub list is the same size as board
            for entry in row:
                assert entry == None, 'initialise_board function does not have None values for every entry'
        testReport_c.add_message('test_initialise_board_correct_size passed')
    except:
        testReport_c.add_message('test_initialise_board_correct_size failed')
    
def test_initialise_board_incorrect_input():
    '''
    Tests if initialise_board raises TypeError for non integer input
    ''' 
    try:
        with pytest.raises(TypeError):
            initialise_board('string') #Checks that an non integer input will lead to a type error
        testReport_c.add_message('test_initialise_board_incorrect_input passed')
    except:
        testReport_c.add_message('test_initialise_board_incorrect_input failed')

def test_create_battleships_correct_type():
    '''
    Tests if create_battleships function returns a dictionary with the correct values
    '''
    text_file = 'battleships.txt'
    created_battleships = create_battleships(text_file)
    try:
        assert isinstance(created_battleships,dict), 'created_battleships function does not return a dictionary' #Checks that the return is a list
        testReport_c.add_message('test_create_battleships_correct_type passed')
    except:
        testReport_c.add_message('test_create_battleships_correct_type failed')

def test_create_battleships_correct_values():
    '''
    Tests if create_battleships returns the correct values
    '''
    text_file = 'battleships.txt'
    created_battleships = create_battleships(text_file)
    battleships_result = {'Aircraft_Carrier':5,'Battleship':4,'Cruiser':3, 'Submarine':3,'Destroyer':2}
    try:
        assert created_battleships == battleships_result, 'created_battleships function does not return correct output' #Checks the correct output is returned from the function
        testReport_c.add_message('test_create_battleships_correct_values passed')
    except:
        testReport_c.add_message('test_create_battleships_correct_values failed')

#Where put these files
def test_create_battleships_wrong_format():
    '''
    Tests if errors are raised for incorrect file format
    '''
    text_file_1 = 'test_create_battleships_wrong_format_1.txt' #Files created to have errors this one doesn't have :
    text_file_2 = 'test_create_battleships_wrong_format_2.txt' #File has incorrect values
    try:
        with pytest.raises(IndexError):
         create_battleships(text_file_1)
        with pytest.raises(ValueError):
            create_battleships(text_file_2)
        testReport_c.add_message('test_create_battleships_wrong_format passed')
    except:
        testReport_c.add_message('test_create_battleships_wrong_format failed')
    
def test_place_battleships_correct_size():
    '''
    Tests if place_battleships returns a dictionary of correct size
    '''
    size=10
    empty_board_test = initialise_board(size)
    battleships_test = create_battleships('battleships.txt')
    simple_battleships = place_battleships(empty_board_test,battleships_test,'simple')
    try:
        assert isinstance(simple_battleships,list), 'place_battleships function does not return a dictionary' #Checks that the return is a dictionary
        assert len(simple_battleships) == size, 'place_battleships fucntion does not return lists of correct size' #Checks the size of the return is as required
        testReport_c.add_message('test_place_battleships_correct_size passed')
    except:
        testReport_c.add_message('test_place_battleships_correct_size failed')


def test_place_battleships_wrong_custom_file():
    '''
    Tests if place_battleships raises a Type error with an incorrect 
    file in custom_file argument
    '''
    size=10
    empty_board_test = initialise_board(size)
    battleships_test = create_battleships('battleships.txt')
    try:
        with pytest.raises(TypeError):
            place_battleships(empty_board_test,battleships_test,'custom',(123)) #Checks if valid JSON file not provided, it will raise a Type Error
        testReport_c.add_message('test_place_battleships_wrong_custom_file passed')
    except:
        testReport_c.add_message('test_place_battleships_wrong_custom_file failed')

def test_place_battleships_wrong_placement():
    '''
    Tests if place_battleships raises a Value Error if incorrect value is used
    '''
    size=10
    empty_board_test = initialise_board(size)
    battleships_test = create_battleships('battleships.txt')
    try:
        with pytest.raises(TypeError):
            place_battleships(empty_board_test,battleships_test,'not simple') #Checks an invalid placement value will lead to a ValueError
        testReport_c.add_message('test_place_battleships_wrong_placement passed')
    except:
        testReport_c.add_message('test_place_battleships_wrong_placement failed')


def test_place_battleships_wrong_dictionary_type():
    '''
    Tests if place_battleships raises a Type Error if incorrect type is entered as an argument
    '''
    try:
        with pytest.raises(AttributeError):
            place_battleships([],'not a dictionary')
        testReport_c.add_message('test_place_battleships_wrong_argument_type passed')
    except:
        testReport_c.add_message('test_place_battleships_wrong_argument_type failed')

def test_place_battleships_too_many_ships():
    '''
    Tests if place_battleships raises a Type Error if the board cannot fit
    all of the ships
    '''
    board = [[None]] #Sets a board with one space
    ships_too_big = {'Test_ship':3} #Size of ship is bigger than space available
    try:
        with pytest.raises(TypeError):
            place_battleships(board = board, ships = ships_too_big)
        testReport_c.add_message('test_place_battleships_too_many_ships passed')
    except:
        testReport_c.add_message('test_place_battleships_too_many_ships failed')



test_initialise_board_correct_size()
test_initialise_board_incorrect_input()
test_create_battleships_correct_type()
test_create_battleships_correct_values()
test_create_battleships_wrong_format()
test_place_battleships_correct_size()
test_place_battleships_wrong_custom_file()
test_place_battleships_wrong_placement()
test_place_battleships_wrong_dictionary_type()
test_place_battleships_too_many_ships()
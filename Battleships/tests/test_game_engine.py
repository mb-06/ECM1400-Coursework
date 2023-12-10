from components import initialise_board,create_battleships
from game_engine import attack
import pytest

import test_helper_functions as thf #Using provided module to provide report
testReport_ge = thf.TestReport("test_game_engine_report.txt")

def test_attack_return_type():
    '''
    Tests if attack returns a boolean response 
    '''
    coordinates = (0,1)
    board = initialise_board()
    battleships = create_battleships()
    try:
        assert isinstance(attack(coordinates,board,battleships),bool), "attack function doesn't return a boolean value"
        testReport_ge.add_message('test_attack_return_type passed')
    except:
        testReport_ge.add_message('test_attack_return_type failed')

def test_attack_return_hit():
    '''
    Tests if attack returns True if a ship is hit and dictionary is updated
    '''
    coordinates = (0,0)
    board = [['test_ship']]
    battleships = {'test_ship':1}
    func_result = attack(coordinates,board,battleships)
    try:
        assert func_result == True, "attack function doesn't return True when a ship is hit" #Tests if True is returned when a ship is hit
        ship_numbers  = all(value == 0 for value in battleships.values()) #Checks if value in dictionary is updated
        assert ship_numbers == True, "attack function doesn't update dictionary"
        testReport_ge.add_message('test_attack_return_hit passed') 
    except:
        testReport_ge.add_message('test_attack_return_hit failed')

def test_attack_return_miss():
    '''
    Tests if attack returns False if a ship is missed 
    '''
    coordinates = (0,0)
    battleships = {'test_ship':1}
    board = [[None]]
    func_result = attack(coordinates,board,battleships)
    try:
        assert func_result == False, "attack function doesn't return True when a ship is hit" #Tests if True is returned when a ship is hit
        testReport_ge.add_message('test_attack_return_miss passed')
    except:
        testReport_ge.add_message('test_attack_return_miss failed')

    
def test_attack_incorrect_size():
    '''
    Tests if attack raise a Value Error if tuple is not the right size
    '''
    coordinates = (0,0,0)
    battleships = {'test_ship':1}
    board = [[None]]
    try:
        with pytest.raises(ValueError):
            attack(coordinates,board,battleships)
        testReport_ge.add_message('def test_attack_incorrect_size passed')
    except:
        testReport_ge.add_message('def test_attack_incorrect_size failed')


test_attack_incorrect_size()
test_attack_return_hit()
test_attack_return_miss()
test_attack_return_type()
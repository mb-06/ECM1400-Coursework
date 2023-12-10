from mp_game_engine import generate_attack
import pytest

import test_helper_functions as thf #Using provided module to provide report
testReport_mge = thf.TestReport("test_mp_game_engine_report.txt")

def test_generate_attack_correct_type():
    '''
    Tests if generate_attack returns a tuple of correct size
    '''
    board = [[0,1],[0,1],[0,1]]
    attacked_points = []
    point = generate_attack(board,attacked_points)
    try:
        assert isinstance(point,tuple), 'generate_attack function does not return a tuple'
        assert len(point) == 2, 'generate_attack does not return correct length' #Tuple needs to be coordinates (y,x)
        for i in point:
            assert isinstance(i,int), 'generate_attack returns tuple with inputs too long' #If not an integer, it will be too long
        testReport_mge.add_message('test_generate_attack_correct_type passed')
    except:
        testReport_mge.add_message('test_generate_attack_correct_type failed')



def test_generate_attack_unique_guess():
    '''
    Tests if generate_attack returns a unique guess
    '''
    board = [[0,1],[0,1],[0,1]]
    attacked_points = [(0,0)] #Creating list that says (0,0) has been attacked
    point = generate_attack(board,attacked_points)
    try:
        assert point != (0,0), 'generate_attack function does not return a unique guess' #As we have already attacked (0,0), it shouldn't be returned
        testReport_mge.add_message('test_generate_attack_unique_guess passed')
    except:
        testReport_mge.add_message('test_generate_attack_unique_guess failed')


def test_generate_attack_incorrect_inputs():
    '''
    Tests if generate_attack raises a Type Error when given incorrect arguments
    '''
    board = [[0,1],[0,1],[0,1]]
    attacked_points = 'test' #Setting attacked_points to incorrect argument
    try:
        with pytest.raises(TypeError):
            generate_attack(board,attacked_points)
        board = 'test' #Setting board to incorrect argument
        attacked_points = [(0,0)]
        with pytest.raises(TypeError):   
            generate_attack(board,attacked_points)
        testReport_mge.add_message('test_generate_attack_incorrect_inputs passed')
    except:
        testReport_mge.add_message('test_generate_attack_incorrect_inputs failed')

test_generate_attack_correct_type()
test_generate_attack_unique_guess()
test_generate_attack_incorrect_inputs()
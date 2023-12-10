from flask import Flask
from flask import request
from flask import render_template
from flask.json import jsonify 
from components import initialise_board,create_battleships,place_battleships
from game_engine import attack 
from mp_game_engine import generate_attack
import logging 

app = Flask(__name__)

#Difficulty levels not implemented into flask

board =[[]]


@app.route('/placement',methods=['GET','POST'])
def placement_interface():
    '''
    Accept a post request containing the players board in the form of a config.json
    also accepts a get request which return placement.html template with a ships dictionary a baord size list
    '''
    global ships #Uses global to uses ships in next function
    global empty_board
    ships = create_battleships() #Gets the battleships from file
    empty_board = initialise_board() #initialises empty board
    board_size = len(empty_board)
    empty_board_ai = initialise_board() #Creates board for ai
    global ships_ai #Uses global to uses ships in next function
    global ai_board #Uses global to uses ships in next function
    ships_ai = create_battleships() # creates dictionary for ai
    ai_board = place_battleships(empty_board_ai,ships_ai,'random') #places ships for ai
    if request.method == 'GET':
        logging.info('Template rendered')
        return render_template('placement.html',ships=ships,board_size=board_size) 
    if request.method == 'POST':
        global placements
        placements = request.get_json() #Receives json from the placements by user
        global board
        board = place_battleships(empty_board,ships,'custom',placements)
        logging.info('Json file received')
        return jsonify({"message":"success"})    #Show success message and allows redirect
    


@app.route('/',methods=['GET'])
def route():
    '''
    Accepts a get request to render template main.html with a player board list
    '''
    logging.info('Template rendered')
    return render_template('main.html',player_board=board)

attacks_by_user =[]
attacked_points = [] #Set to allow AI to make new guesses each time


@app.route('/attack',methods=['GET'])
def process_attack():
    '''
    Accepts a get request to get the coordinates to be attacked by the user. This then will run the game against
    the AI until someone wins
    '''
    if request.args:
        x = request.args.get('x') #Gets the x and y coordinate
        y = request.args.get('y')
        logging.info('Coordinates received')
        if (y,x) in attacks_by_user: #Checks if it is unique
            logging.info('Coordinates already guessed')
            return jsonify({'hit':False}) #Here by the definition of the coursework, it will definetely be None
        else:
            ai = generate_attack(board,attacked_points) #Generates AI hit, this will update attacked_points
            did_hit_user = attack((y,x),ai_board,ships_ai) #Sees if user hits
            attack(ai,board,ships) #AI attacks user
            attacks_by_user.append((y,x)) #Adds to list of guesses by user    
        game_finished_user_win = all(value == 0 for value in ships_ai.values()) # checks if user wins
        game_finished_ai_win = all(value == 0 for value in ships.values()) #checks if ai wins
        if game_finished_user_win: #returns the required message
                    logging.info('User has won the game')
                    return jsonify({'hit':did_hit_user,'AI_Turn':ai,'finished':'Congrats,you won'})
        if game_finished_ai_win:
            logging.info('AI has won the game')
            return jsonify({'hit':did_hit_user,'AI_Turn':ai,'finished':'Comiserations,you lost'})
        else:
            return jsonify( {'hit':did_hit_user,'AI_Turn':ai })


if __name__ == '__main__':
    logging.basicConfig(filename = 'main.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S' ) #Initialises log file 
    app.template_folder = 'templates'
    app.run()
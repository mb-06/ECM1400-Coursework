# ECM1400 Battleships Coursework

This coursework is a code for the game Battleships. It is written in Python 3, and has three main processes. It allows the user to play the game single player against a pre made board, it allows the user to play against an AI opponent with ASCII representation of the board, and with the use of Flask, there is a web implementation of the game against the AI.


## Getting Started

To be able to use the code, a few packages need to be downloaded. Firstly, for logging throughout the code, the logging package needs to be installed. To do so, write in the command prompt :

![](pictures\logging.png)

For the web implementation of the game, flask is needed. To install use:

![](pictures\flask.png)

For testing the modules within the code, pytest is used. To install use:

![](pictures\pytest.png)

To install the package itself, use pip install:

![](pictures\install.png)


## Functions
For each module, the functions and there capabilities will be listed:
* components.py:
    * initialise_board() - Creates a board of requested size (completed)
    
    * create_battleships() - Creates a dictionary with ship names and their sizes from text file (completed). This file has to be in the form:

    ![t](pictures\textstyle.png)

    * place_battleships() - Places battleships on the board. Can do this in four ways. A simple algorithm, a random algorithm, a custom algorithm(using a JSON file) or an optimised algorithm(used to change difficulty) (completed).

* game_engine.py:
    * attack() - Processes an attack, updating a dictionary and playing board (completed)

    * cli_coordinates_input() -  Requests row and column user wants to attack, and gives a tuple with this (completed)

    * simple_game_loop() - Plays out a simple game, where only the user plays. Here, the simple algorithm of placement us used (completed)

* mp_game_engine.py:
    * generate_attack() - Generates random attack on a set board (completed)

    * ai_opponent_game_loop() - Plays out a game against an AI, where the difficulty can be set (completed). Also has an ASCII representation:

    ![](pictures\ASCII.png)

* main.py:
    * placement_interface() - Accept a post request containing the players board in the form of a config.json
    also accepts a get request which return placement.html template with a ships dictionary a baord size list (completed)

    * route() - Accepts a get request to render template main.html with a player board list(completed)

    * process_attack()  - Accepts a get request to get the coordinates to be attacked by the user. This then will run the game against the AI until someone wins(completed)

    * In main.py the difficulty cannot be set

## Testing
Testing can be carried out using the tests provided in the tests folder. Each module has a list of tests, which can be accesed in **tests_module-name.py** where module-name is components, game_engine or mp_game_engine (currently no tests for main.py)

## How to use
Here we go through an example of how to use the package. Note when written to 'run the code', this means (if using an inline interpreter) to call:

![](pictures\module.png)

Also, all images here are from the source code editor VSCode to simplify how to use the modules and present it in a easier way. Similiar things can be done in an in-line interpreter.

We start in components.py, where we can call initialise_board() and create_battleships() to put into place_battleships(). Here, for each function, default values are used, but note this can be changed

![](pictures\components.png)

This will return a simple board. The third argument can be changed to random, custom (requiring a JSON file) or optimised.

Using the game_engine module, all you have to do is run the code. It will the run a simple game loop, where you will be requsted to enter a row and column. If these don't fit the board, are not integers or have already been guessed, you will be asked again. This will end when the game finishes, or you enter q:

![](pictures\game_engine.png) 

Using the mp_game_engine module, all you have to do is run the code. This will request the difficulty level, and then present your board (which is based on a preset JSON file). Then you will be requested to enter the coordinates you want to attack. It will attack the AI, and produce an AI attack on you. The user attacks are shown on your board, X for a hit and * for a miss. The game will end when the user wins, the AI wins or the user quits the game by inputting q.

![](pictures\mp_game_engine1.png)

![](pictures\mp_game_engine2.png)

Using the main module, run the module either from a source code editor, or an in-line interpreter by:

![](pictures\main1.png)

Here you may be given a link to press. If not, as shown, on a web browser go to http://127.0.0.1:5000/placement . If you are shown the link, in the browser add /placement to start

![](pictures\main2.png)

Here you will be shown a board. You can place a board by clicking on a box when it shows a green ship. Having placed all the boards, press start game.

![](pictures\main3.png)

Then, you will be shown an empty board to attack. Press on the board to attack. If it goes red, it has hit a ship, if it goes blue it has missed. The AI will attack and this can be seen on the right hand of the screen.

![](pictures\main4.png)

When either the user wins or the AI wins, a message will be displayed at the top of the screen. To play again, rerun the main.py module.

![](pictures\main5.png)

To test, run the tests that you want to run in the same format as before. This will then create a report, which can be accessed in the testing files. if problems occur, this may be due to file location problems. Simply move the tests into the game file, and they will work 

## License
This project was realeased under the BSD (Berkeley Software Distribution) 2-Clause license

## Author
Matthew Bright

## Acknowledgements
When researching how to optimise the placement algorithm, a few sources where used:
* https://www.instructables.com/How-to-Win-at-Battleship/
* https://www.thesprucecrafts.com/how-to-win-at-battleship-411068

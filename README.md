# AIA_gomoku_2019
3rd year artificial intelligence project in Python in which the goal is to implement a Gomoku Narabe game bot/ai.
It is a 2-player game that is played on a 19x19 game board by default (20x20 on "Piskvork"). Each player plays a stone at his/her turn, and the game ends as soon as one has a 5 stones in a row (vertically, horizontally or diagonaly) and thus wins.
The bot is compliant with the communication protocol and can be upload on "Piskvork" (windows Gomoku software plateform).
The program is built using the Min-max method and can be played against a human and ai player. Other than on Piskvork it can also be manually tested on Linux/Macos with commands sequences detailed below.

USAGE :

./pbrain-minMax.py

COMMANDS :

START [size >= 20] - Select board sizes.

BEGIN - To start the game.

TURN [X],[Y] - The parameters are coordinate of the opponent's move. All coordinates are numbered from zero.

BOARD - This command imposes entirely new playing field. It is suitable for continuation of an opened match or for undo/redo user commands.
After this command the data forming the playing field are send. Every line is in the form:
 [X],[Y],[field]
where [X] and [Y] are coordinates and [field] is either number 1 (own stone) or number 2 (opponent's stone) or number 3 (only if continuous game is enabled, stone is part of winning line or is forbidden according to renju rules).
Then Data are ended by DONE command.

INFO [key] [value] - Informations about the current game (time remaining in the game, time remaining for each moves...) :

The key can be:
timeout_turn  - time limit for each move (milliseconds, 0=play as fast as possible)
timeout_match - time limit of a whole match (milliseconds, 0=no limit)
max_memory    - memory limit (bytes, 0=no limit)
time_left     - remaining time limit of a whole match (milliseconds)
game_type     - 0=opponent is human, 1=opponent is brain, 2=tournament, 3=network tournament
rule          - bitmask or sum of 1=exactly five in a row win, 2=continuous game, 4=renju
evaluate      - coordinates X,Y representing current position of the mouse cursor
folder        - folder for persistent files

Example:

 > INFO timeout_match 300000
 
 > INFO timeout_turn 10000
 
 > INFO max_memory 83886080

 >Expected answer: none
 
 END - To end the current game.
 
 ABOUT - Informations about the current player such as author, country, www, email etc...
 
 More detailed commands can be found here : https://svn.code.sf.net/p/piskvork/code/trunk/source/doc/protocl2en.htm

![Image description](pic/illustration.png)

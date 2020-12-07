---------------------------------------------------------------------------------------------
--------------------------------------MINESWEEPER-------------------------------------
---------------------------------------------------------------------------------------------


Game Rules According to Wikipedia @ https://en.wikipedia.org/wiki/Minesweeper_(video_game)

	“In Minesweeper, mines are scattered throughout a board which is divided into cells. Cells have three states: uncovered, covered, and flagged. A covered cell is blank and clickable, while an uncovered cell is exposed. Flagged cells are those marked by the player to indicate a potential mine location. 

A player left clicks a cell to uncover it. If a player uncovers a mined cell, the game ends. Otherwise, the uncovered cells display either a number, indicating the quantity of mines adjacent to it, or a blank tile (or "0"), and all adjacent non-mined cells will automatically be uncovered. Right-clicking on a cell will flag it, causing a flag to appear on it. Flagged cells are still covered, and a player can click on them to uncover them, although typically they must first be unflagged with an additional right-click. 

To win the game, players must uncover all non-mine cells, at which point the timer is stopped. Flagging all the mined cells is not required.”


---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------


To Run the Game:

Visit https://repl.it/talk/share/Minesweeper/84907 and run the repl.it

Resizing the repl.it windows so that the console is made as small as possible will make playing the game much easier.

A 22 x 22 random board is randomly generated with 99 bombs. 

However, the user can edit the code at line 483 to edit difficulty:
	By default it reads "Minesweeper = Board(22, 99)"

	The first parameter determines the size of the board (and should not be tampered with. I did not get to coding this to be dynamic).

	The second paramter determines the 'difficulty' or number of bombs. This can be changed as much as a user likes. 
		99 is decently difficult. 75 is easy. Anything below 60 is very easy. 

Upon a 'loss' (ie. clicking on a bomb), a user can simply press space to randomly generate a new board. 


---------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------

Bonus According to Piazza:

	Randomly generated puzzle each time +1

	GUI +3


I hope you enjoy playing as much as I enjoyed building this game! 

Connor LaCour


---------------------------------------------------------------------------------------------
--------------------------------------MINESWEEPER-------------------------------------
---------------------------------------------------------------------------------------------
#TODO
# Fixa så lösningen är GUI.

import tkinter
import bisect

level = [["E" for i in range(6)] for j in range(8)]
window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=40*6, height=40*8)
output = list();
toPlace = "W"
startPos = [0,0]
currentPos = [0,0]

def checkIfSolved(level):
	for row in level:
		for column in row:
			if(column == 'E'):
				return False;
	return True;

def solver(currentPos, level):
	global output
	#Try moving downwards.
	if(currentPos[0] + 1 < 8):
		if(level[currentPos[0] + 1][currentPos[1]] != 'W' and level[currentPos[0] + 1][currentPos[1]] != 'P'):
			#Move down
			currentPos[0] = currentPos[0] + 1;
			level[currentPos[0]][currentPos[1]] = 'P';
			#If level complete
			if(solver(currentPos, level)):
				output.append("DOWN");
				return True;
			#Else we undo the move.
			else:
				#Remove the player block and move the currentPos.
				level[currentPos[0]][currentPos[1]] = 'E';
				currentPos[0] = currentPos[0] - 1;
	#Try moving upwards.
	if(currentPos[0] - 1 >= 0):
		if(level[currentPos[0] - 1][currentPos[1]] != 'W' and level[currentPos[0] - 1][currentPos[1]] != 'P'):
			#Move up
			currentPos[0] = currentPos[0] - 1;
			level[currentPos[0]][currentPos[1]] = 'P';
			#If level complete
			if(solver(currentPos, level)):
				output.append("UP");
				return True;
			#Else we undo the move.
			else:
				#Remove the player block and move the currentPos.
				level[currentPos[0]][currentPos[1]] = 'E';
				currentPos[0] = currentPos[0] + 1;
	#Try moving right.
	if(currentPos[1] + 1 < 6):
		if(level[currentPos[0]][currentPos[1] + 1] != 'W' and level[currentPos[0]][currentPos[1] + 1] != 'P'):
			#Move right
			currentPos[1] = currentPos[1] + 1;
			level[currentPos[0]][currentPos[1]] = 'P';
			#If level complete
			if(solver(currentPos, level)):
				output.append("RIGHT");
				return True;
			#Else we undo the move.
			else:
				#Remove the player block and move the currentPos.
				level[currentPos[0]][currentPos[1]] = 'E';
				currentPos[1] = currentPos[1] - 1;
	#Try moving left.
	if(currentPos[1] - 1 >= 0):
		if(level[currentPos[0]][currentPos[1] - 1] != 'W' and level[currentPos[0]][currentPos[1] - 1] != 'P'):
			#Move left
			currentPos[1] = currentPos[1] - 1;
			level[currentPos[0]][currentPos[1]] = 'P';
			#If level complete
			if(solver(currentPos, level)):
				output.append("LEFT");
				return True;
			#Else we undo the move.
			else:
				#Remove the player block and move the currentPos.
				level[currentPos[0]][currentPos[1]] = 'E';
				currentPos[1] = currentPos[1] + 1;
	#We come here if we have nowhere to go. Check if we have solved it.
	return checkIfSolved(level);

# Where should a wall be placed?
def placeObject(x, y, type):
	global currentPos
	global startPos
	posX, posY = bisect.bisect_left([40, 80, 120, 160, 200], x), bisect.bisect_left([40, 80, 120, 160, 200, 240, 280], y)
	level[posY][posX] = type
	if type == "W":
		canvas.create_rectangle(40*posX, 40*posY, 40*posX+40, 40*posY+40, fill="black")
	else:
		currentPos = [posY,posX]
		startPos = [posY,posX]
		canvas.create_oval(40*posX, 40*posY, 40*posX+40, 40*posY+40, fill="red")

def changeToPlace(val):
	global toPlace
	toPlace = val

def solveGUI(output):
	global canvas
	global startPos
	for i in output:
		if i == "UP":
			canvas.create_line(40*startPos[1]+20, 40*startPos[0] - 20, 40*startPos[1] + 20, 40*startPos[0] + 20, fill="red")
			startPos[0] -= 1
		elif i == "DOWN":
			canvas.create_line(40*startPos[1]+20, 40*startPos[0] + 20, 40*startPos[1] + 20, 40*startPos[0] + 60, fill="red")
			startPos[0] += 1
		elif i == "LEFT":
			canvas.create_line(40*startPos[1] - 20, 40*startPos[0]+20, 40*startPos[1] + 20, 40*startPos[0]+20, fill="red")
			startPos[1] -= 1
		elif i == "RIGHT":
			canvas.create_line(40*startPos[1] + 20, 40*startPos[0]+20, 40*startPos[1]+60, 40*startPos[0]+20, fill="red")
			startPos[1] += 1

def solvePuzzle():
	global currentPos
	global level
	global output
	solver(currentPos, level);
	output = list(reversed(output));
	solveGUI(output);

def main():
	global window
	global level
	global currentPos
	global canvas
	global toPlace
	window.wm_title("Solver")
	canvas.bind("<Button-1>", lambda event: placeObject(event.x, event.y, toPlace))
	canvas.pack()
	for columnIndex, column in enumerate(level):
		for rowIndex, row in enumerate(column):
			circle = canvas.create_oval(rowIndex*40, columnIndex*40, rowIndex*40+40, columnIndex*40+40, fill="white")
	solveButton = tkinter.Button(window, text="Solve puzzle", command = lambda: solvePuzzle())
	solveButton.pack(side="bottom")
	playerButton = tkinter.Button(window, text="Place player", command = lambda: changeToPlace("P"))
	playerButton.pack(side="bottom")
	window.mainloop()

if __name__ == '__main__': main()

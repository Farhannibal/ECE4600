# Library of command
def listOfCommand(command):
	return{
		"UP":1,
		"DOWN":2,
		"LEFT":3,
		"RIGHT":4,
		"STOP":5
	}.get(command, 9) # default will be WAIT
from gpiozero import LED, Button
from signal import pause
from time import time
from time import sleep
from random import randint
import sys
import MySQLdb	

try:
	db = MySQLdb.connect("localhost","assignmentuser","123456","CA1Database")
	curs = db.cursor()
	print("Successfully connected to database!")
except:
	print("Error connecting to mySQL database")	





ledRed = LED(18)
ledYellow = LED(22)
ledGreen = LED(17)
ledMaintain = LED(5)
buttonRight = Button(13, pull_up=False)
buttonLeft = Button(20, pull_up=False)

score = 0
pattern = 0
DIFFICULTY = 2

old_time = time()
lose = False
waitButton = False
buttonDisabled = False

restartMenu = False
restart = True


def updateDatabase(inscore):
	try:

		print("Saving score to Database... ")
		sql = "INSERT into arcadeData (score) VALUES (%s)" % inscore
		print(sql)
		curs.execute(sql)
		db.commit()
		print("Commited To Database")
		sleep(1)
	except MySQLdb.Error as e:
		print e


def disableButton():
	global buttonDisabled
	buttonDisabled = True
def enableButton():
	global buttonDisabled
	buttonDisabled = False

def offBothLED():
	ledYellow.off()
	ledRed.off()

def getRestartInput():
	disableButton()
	gameOver()
	global restartMenu
	restartMenu = True
	sleep(2)
	enableButton()
	print("Press the RED button to restart the game, press the YELLOW button to exit.")
	userInput = False
	offBothLED()
	while userInput==False:
		if buttonRight.is_pressed:
			disableButton()
			print("Restarting game in 3 seconds...")
			sleep(3)
			enableButton()
			restartLevel(True)
			global score
			score = 0
			global lose
			lose=False
			userInput = True
			restartMenu = False	
					

		elif buttonLeft.is_pressed:
			userInput = True
			restartLevel(False)
			restartMenu = False
			ledGreen.off()
			
			curs.close()
			db.close()



	
def restartLevel(input):
	global restart
	restart = input


def onYellow():
	ledYellow.on()
def onRed():
	ledRed.on()
def onBoth():
	ledYellow.on()
	ledRed.on()

ledSwitch = {0 : onYellow,
	     1 : onRed,
	     2 : onBoth,
	}

#set the difficulty of the game by adjusting the speed
def setDifficulty():
	global DIFFICULTY
	if score < 10:
		#EASY LEVEL
		DIFFICULTY = 2
	elif score < 20:
		#MEDIUM LEVEL
		DIFFICULTY = 1.2
	elif score < 30:
		#HARD LEVEL
		DIFFICULTY = 0.8
	elif score < 50:
		#INSANE LEVEL
		DIFFICULTY = 0.5
	

def gameOver():
	print("Game Lost!")
	print("Final score: " + str(score))
	updateDatabase(score)
	ledGreen.blink()
	
def checkMaintenance():
	if ledMaintain.is_lit:
		print("Maintenance is ongoing now, game is stopped.")

def pushYellowLED():
	checkMaintenance()
	#buttons are able to be pressed
	if buttonDisabled == False:
		#not inside restart menu
		if restartMenu == False:
			global lose
			#if yellow led is on during game
			if ledYellow.is_lit and lose==False:
				print("pushedYellowButton")
				ledYellow.off()
				
				if ledRed.is_lit:
					#global old_time
					#old_time = time()
					waitButton = True
				else: 
					global score 
					score = score + 2
					waitButton = False
			else:
				lose = True


def pushRedLED():
	checkMaintenance()
	#buttons are able to be pressed
	if buttonDisabled == False:
		#not inside restart menu
		if restartMenu == False:
			global lose
			#if red led is on during game
			if ledRed.is_lit and lose==False:
				print("pushedRedButton")
				ledRed.off()
				if ledYellow.is_lit:
					#global old_time
					#old_time = time()
					waitButton = True
				else: 
					global score 
					#edit score as you like
					score = score + 2
					waitButton = False
			else:
				lose = True


buttonRight.when_pressed = pushRedLED
buttonLeft.when_pressed = pushYellowLED

def checkLevelCleared():
	if ledRed.is_lit or ledYellow.is_lit:
		getRestartInput()

disableButton()
#introduction
print("WELCOME to TAP TAP 1.0! THE GAME WILL START IN 3 SECONDS!!")

ledMaintain.off()

sleep(3)
enableButton()
#loop infinitely
while restart:

	if ledMaintain.is_lit == False:
	
		#shows gameplay started
		ledGreen.on()
	
		#generate a pattern
		pattern = randint(0,2)
		print("score= " + str(score) + " Pattern= " + str(pattern))
		
		#Switch statement that triggers different pattern
		ledSwitch[pattern]()
	
		#set the difficulty based on score
		setDifficulty()
		
		
		#the number determine the seconds (difficulty)
		sleep(DIFFICULTY)
		
		#ensure all led lights are offed
		checkLevelCleared()
		

	

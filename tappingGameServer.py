import datetime
import gevent
import gevent.monkey
from gevent.pywsgi import WSGIServer

gevent.monkey.patch_all()

from flask import Flask, request, Response, render_template
from gpiozero import LED

import MySQLdb	

try:
	db = MySQLdb.connect("localhost","assignmentuser","123456","CA1Database")
	curs = db.cursor()
	print("Successfully connected to database!")
except:
	print("Error connecting to mySQL database")	

led = LED(5)

def ledOn():
	led.on()
	return "LED has been turned on"
def ledOff():
	led.off()
	return "LED has been turned off"

def ledStatus():
	if led.is_lit:
		return 'On'
	else:
		return 'off'

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/readLED/")
def readPin():

	response = ledStatus()
	templateData = {
		'title' : 'Status of LED',
		'response' : response
	}
	return render_template('pin.html',**templateData)

@app.route("/writeLED/<status>")
def writePin(status):

	if status == 'On':
		response = ledOn()
	else:
		response = ledOff()

	templateData={
		'title' : 'Status of LED',
		'response' : response
	}

	return render_template('pin.html',**templateData)

if __name__ == '__main__':
	try:
		http_server = WSGIServer(('0.0.0.0',8001),app)
		app.debug = True
		http_server.serve_forever()
	except:
		print("Exception")


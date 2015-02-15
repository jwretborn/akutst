import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
  return 'Hello World! 2'

@app.route("/bye")
def bye():
	return 'Bye Bye'


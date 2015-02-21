import os
import time
import psycopg2
import urlparse
from flask import Flask, request, redirect, url_for
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DATABASE_URL='] = "postgresql://localhost/akutst"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://localhost/akutst"
app.debug = True
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
	d = time.strftime("%Y-%m-%d")
	return render_template('form.html', date_today=d)

@app.route('/procedure', methods=['GET', 'POST'])
def procedure():
	errors = []
	if request.method == 'POST':

		p = Procedure(
			user_id=request.form['user_id'],
			type=request.form['procedure'],
			created=request.form['date'],
			successful=request.form['successful'],
			attempts=request.form['attempts']
		)
		db.session.add(p)
		db.session.commit()

		return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    app.run()
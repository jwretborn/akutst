import os
import time
import psycopg2
import urlparse
import json
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

from models import *

@app.route("/")
def index():
	d = time.strftime("%Y-%m-%d")
	procedure_types = db.session.query(ProcedureType).all()
	return render_template('form.html', date_today=d, procedures=procedure_types)

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

		flash(u'Proceduren sparad', 'info')

		return redirect(url_for('index'))
	else:
		return redirect(url_for('index'))

@app.route('/diagnostic', methods=['GET', 'POST'])
def diagnostic():
	return redirect(url_for('index'))

@app.route('/group/<id>/items', methods=['GET'])
def group_items(id):
	query = db.session.query(Group).filter(Group.id == id)
	group = query.first()
	items = db.session.query(GroupItem).filter(GroupItem.group_id == group.id).all()
	return jsonify(items=[i.serialize for i in items])

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    app.run()
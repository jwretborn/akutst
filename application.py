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
	return redirect(url_for('procedure'))

@app.route("/ultraljud")
def ultrasound():
	return render_template('diagnostics.html')

@app.route("/patienter")
def patients():

	if request.method == 'POST':
		try :
			p = Patient(
			)
			db.session.add(p)
			db.session.commit()

			flash(u'Proceduren sparad', 'info')
		except:
			flash(u'Something went wrong', 'warning')

	d = time.strftime("%Y-%m-%d")
	ages = []
	levels = []
	codes = []

	ages = db.session.query(GroupItem).filter(GroupItem.group_id == 27) ### Hack
	levels = db.session.query(GroupItem).filter(GroupItem.group_id == 26) ### Hack
	codes = db.session.query(GroupItem).filter(GroupItem.group_id == 28)

	return render_template("patients.html", date_today=d, ages=ages, levels=levels, codes=codes)

@app.route('/procedurer', methods=['GET', 'POST'])
@app.route('/procedurer/<id>', methods=['GET', 'POST'])
def procedure(id=False):
	errors = []
	procedure_type = False
	if request.method == 'POST':
		try :
			p = Procedure(
				user_id=request.form['user_id'],
				type=request.form['procedure'],
				method=request.form['method'],
				anatomy=request.form['anatomy'],
				tuition=request.form['tuition'],
				created=request.form['date'],
				successful=request.form['successful'],
				comments=request.form['comments']
			)
			db.session.add(p)
			db.session.commit()

			flash(u'Proceduren sparad', 'info')
		except:
			flash(u'Something went wrong', 'warning')

	d = time.strftime("%Y-%m-%d")
	p_types = db.session.query(ProcedureType).all()
	procedure_type = p_types[0]

	methods = []
	anatomy = []

	if procedure_type.method_group is not None :
		methods = db.session.query(GroupItem).filter(GroupItem.group_id == procedure_type.method_group)

	if procedure_type.anatomy_group is not None :
		anatomy = db.session.query(GroupItem).filter(GroupItem.group_id == p_types[0].anatomy_group)
	
	return render_template('form.html', date_today=d, p_type=procedure_type, procedures=p_types, methods=methods, anatomys=anatomy)

@app.route('/diagnostic', methods=['GET', 'POST'])
def diagnostic():
	return redirect(url_for('index'))

@app.route('/api/procedure', methods=['GET'])
@app.route('/api/procedure/<id>', methods=['GET'])
def api_procedure(id=False):
	if id :
		procedure = db.session.query(Procedure).filter(Procedure.id == id).first()
		return jsonify(procedure.serialize)
	else :
		procedures = db.session.query(Procedure).all()
		return jsonify(items=[i.serialize for i in procedures])

@app.route('/api/proceduretype', methods=['GET'])
@app.route('/api/proceduretype/<id>', methods=['GET'])
def api_procedure_type(id=False):
	if id :
		procedure_type = db.session.query(ProcedureType).filter(ProcedureType.id == id).first()
		return jsonify(procedure_type.serialize)
	else :
		procedure_types = db.session.query(ProcedureType).all()
		return jsonify(items=[i.serialize for i in procedure_types])

@app.route('/api/group/<id>/items', methods=['GET'])
def group_items(id):
	query = db.session.query(Group).filter(Group.id == id)
	group = query.first()
	items = db.session.query(GroupItem).filter(GroupItem.group_id == group.id).all()
	return jsonify(items=[i.serialize for i in items])

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    app.run()
import time
import psycopg2
import urlparse
import json
from os import environ, path
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask import render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from flask_webpack import Webpack


app = Flask(__name__)

here = path.dirname(path.realpath(__file__))
app.config.from_object(environ['APP_SETTINGS'])
debug = "DEBUG" in environ
db = SQLAlchemy(app)

webpack = Webpack()
webpack.init_app(app)

from models import *
from forms import ProcedureForm, PatientForm

@app.route("/")
def index():
	return redirect(url_for('procedure'))

@app.route("/ultraljud")
def ultrasound():
	return render_template('diagnostics.html')

@app.route("/patienter", methods=['GET', 'POST'])
def patients():
	form = PatientForm(request.form)
	if request.method == 'POST' and form.validate() :
		try :
			username = form.user_id.data
			user = db.session.query(User).filter(User.username == username).first()
			
			if user is None:
				raise ValueError(u'ID existerar inte')

			p = Patient(
				user_id=user.id,
				age_id=form.age.data,
				triage_id=form.prio.data,
				retts_id=form.retts.data,
				admittance=form.admittance.data,
				tuition=form.tuition.data,
				comments=form.comments.data,
				created=form.date.data
			)
			db.session.add(p)
			db.session.commit()
			flash(u'Patienten sparad', 'success')
		except ValueError as err:
			flash(err, 'warning')
	else :
		flash_form_errors(form)


	ages = []
	levels = []
	codes = []
	d = time.strftime("%Y-%m-%d")
	
	ages = db.session.query(GroupItem).filter(GroupItem.group_id == 27) ### Hack
	levels = db.session.query(GroupItem).filter(GroupItem.group_id == 26) ### Hack
	codes = db.session.query(RettsCode).all()
	
	return render_template("patients.html", date_today=d, ages=ages, levels=levels, codes=codes)

@app.route('/procedurer', methods=['GET', 'POST'])
@app.route('/procedurer/<id>', methods=['GET', 'POST'])
def procedure(id=False):
	procedure_type = False
	form = ProcedureForm(request.form)
	if request.method == 'POST' and form.validate():
		try :
			## Fetch user
			username = form.user_id.data
			user = db.session.query(User).filter(User.username == username).first()

			if user is None:
				raise ValueError(u'ID existerar inte')

			p = Procedure(
				user_id=user.id,
				type=form.procedure.data,
				method=form.method.data,
				anatomy=form.anatomy.data,
				tuition=form.tuition.data,
				created=form.date.data,
				successful=form.successful.data,
				comments=form.comments.data
			)
			db.session.add(p)
			db.session.commit()

			flash(u'Proceduren sparad', 'success')
		except ValueError as err:
			flash(err, 'warning')
	else :
		flash_form_errors(form)

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

def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Fel %s field - %s" % (getattr(form, field).label.text,error), 'warning')

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

@app.route("/assets/<path:filename>")
def send_asset(filename):
    return send_from_directory(path.join(here, "public"), filename)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
	app.run(extra_files=[app.config["WEBPACK_MANIFEST_PATH"]])
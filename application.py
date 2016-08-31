import time
import psycopg2
import urlparse
import json
from os import environ, path
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask import render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, login_required, current_user
from flask_security.utils import encrypt_password
from flask_webpack import Webpack

from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView
from modules.admin.modelview import MyModelView, PatientModelView, ProcedureModelView, RettsCodeModelView, UserModelView
from modules.admin.view import AnalyticsView

from models import db, User, Patient, Procedure, ProcedureType, RettsCode, Group, GroupItem, Role
from forms import ProcedureForm, PatientForm

# Fix ascii jinja2-error
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

# Setup
here = path.dirname(path.realpath(__file__))
app.config.from_object(environ['APP_SETTINGS'])
debug = "DEBUG" in environ
db.init_app(app)

# Setup Flask-Webpack
webpack = Webpack()
webpack.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

# Setup Flask-admin
admin = Admin(app, name='akutst', template_mode='bootstrap3')
admin.add_view(PatientModelView(Patient, db.session))
admin.add_view(ProcedureModelView(Procedure, db.session))
admin.add_view(MyModelView(ProcedureType, db.session))
admin.add_view(RettsCodeModelView(RettsCode, db.session))
admin.add_view(MyModelView(Group, db.session))
admin.add_view(MyModelView(GroupItem, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))

@app.route("/")
def index():
	return redirect(url_for('patients'))

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

	return render_template('procedure.html', date_today=d, p_type=procedure_type, procedures=p_types, methods=methods, anatomys=anatomy)

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

@app.route('/api/codes', methods=['GET'])
@app.route('/api/codes/<id>', methods=['GET'])
def api_retts_codes(id=False):
	if id :
		code = db.session.query(RettsCode).filter(RettsCode.id == id).first()
		return jsonify(code.serialize)
	else :
		codes = db.session.query(RettsCode).all()
		return jsonify(items=[i.serialize for i in codes])

@app.route('/api/group/<id>/items', methods=['GET'])
def group_items(id):
	try :
		val = int(id)
		query = db.session.query(Group).filter(Group.id == id)
	except ValueError :
		query = db.session.query(Group).filter(Group.name == id)

	group = query.first()
	try :
		items = db.session.query(GroupItem).filter(GroupItem.group_id == group.id).order_by(GroupItem.weight.desc()).all()
	except AttributeError :
		return jsonify({'items' : []})
	return jsonify(items=[i.serialize for i in items])

@app.route('/api/diagnostics/procedures', methods=['GET'])
@login_required
def diagnostic_procedures():
    query = db.session.query(Procedure).filter(Procedure.user_id == current_user.id).all()
    return jsonify(items=[i.serialize for i in query])

@app.route('/api/diagnostics/patients', methods=['GET'])
@login_required
def diagnostic_patients():
	query = db.session.query(Patient).filter(Patient.user_id == current_user.id).all()
	return jsonify(items=[i.serialize for i in query])

@app.route('/api/diagnostics/user', methods=['GET'])
@login_required
def user_join_time():
    user = db.session.query(User).get(current_user.id)
    return jsonify(user.serialize)

@app.route("/assets/<path:filename>")
def send_asset(filename):
    return send_from_directory(path.join(here, "public"), filename)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
	app.run(extra_files=[app.config["WEBPACK_MANIFEST_PATH"]])

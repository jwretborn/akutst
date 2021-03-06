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
from flask_mail import Mail, Message

from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView
from modules.admin.modelview import MyModelView, PatientModelView, ProcedureModelView, RettsCodeModelView, UserModelView
from modules.admin.view import AnalyticsView

from models import db, User, Patient, Procedure, ProcedureType, RettsCode, Group, GroupItem, Role, Tag
from forms import ProcedureForm, PatientForm, ExtendedRegisterForm

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
mail = Mail(app)

# Setup Flask-Webpack
webpack = Webpack()
webpack.init_app(app)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

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
admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
admin.add_view(PatientModelView(Patient, db.session))
admin.add_view(ProcedureModelView(Procedure, db.session))
admin.add_view(MyModelView(ProcedureType, db.session))
admin.add_view(RettsCodeModelView(RettsCode, db.session))
admin.add_view(MyModelView(Group, db.session))
admin.add_view(MyModelView(GroupItem, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

@app.route("/")
def index():
	return redirect(url_for('patients'))

@app.route("/om")
def ultrasound():
	return render_template('about.html')

@app.route("/patienter", methods=['GET', 'POST'])
def patients():
    print request.form
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

            ## Split tag data
            form.tags.data = form.tags.data.split(',')
            add_tags_to_model(form.tags.data, p)

            db.session.add(p)
            db.session.commit()

            flash(u'Patienten sparad', 'success')
        except ValueError as err:
            flash(err, 'warning')
    else :
        flash_form_errors(form)

    return render_template("patients.html")

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

            ## Split tag data
            form.tags.data = form.tags.data.split(',')
            add_tags_to_model(form.tags.data, p)

            db.session.add(p)
            db.session.commit()

            flash(u'Proceduren sparad', 'success')
        except ValueError as err:
            flash(err, 'warning')
    else :
        flash_form_errors(form)

    return render_template('procedure.html')

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

@app.route('/api/tags', methods=['GET', 'POST'])
def api_tags():
    try :
        if request.method == 'POST':
            print request.data
            return jsonify(request.data)
        else :
            tags = db.session.query(Tag).all()
            return jsonify(items=[i.serialize for i in tags])
    except AttributeError:
        return jsonify({'items' : []})


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

# Helper urls
@app.route("/mail/test")
@login_required
def test_mail():
    msg = Message("Hello", recipients=["jens_register@wbn.se"])
    msg.body = "Testing"
    mail.send(msg)
    flash(u'Mail skickat', 'success')
    return redirect(url_for('patients'))

@app.route("/util/reset/<table>", methods=['GET'])
@login_required
def reset_database_seq(table):
    result = db.engine.execute("SELECT setval('%s_id_seq', (SELECT MAX(id) FROM %s)+1)" % (table, table))
    return jsonify("success")

def add_tags_to_model(tag_data, model):
    for tag in tag_data :
        ## Check if we have an integer
        try :
            if isinstance(tag, int) :
                t = db.session.query(Tag).filter(Tag.id == tag).first()
            else :
                t = db.session.query(Tag).filter(Tag.name==tag).first()
                if t is None :
                    t = Tag(
                        name = tag
                    )
                    db.session.add(t)
        except Exception as err :
            flash(err, 'warning')

        if t is not None :
            model.tags.append(t)

# ACME letsencrypt stuff via sabayon https://github.com/dmathieu/sabayon
def find_key(token):
    if token == environ.get("ACME_TOKEN"):
        return environ.get("ACME_KEY")
    for k, v in environ.items():  #  os.environ.iteritems() in Python 2
        if v == token and k.startswith("ACME_TOKEN_"):
            n = k.replace("ACME_TOKEN_", "")
            return environ.get("ACME_KEY_{}".format(n))  # os.environ.get("ACME_KEY_%s" % n) in Python 2

@app.route("/.well-known/acme-challenge/<token>")
def acme(token):
    key = find_key(token)
    if key is None:
        abort(404)
    return key

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
	app.run(extra_files=[app.config["WEBPACK_MANIFEST_PATH"]])

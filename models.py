from application import db
from sqlalchemy.dialects.postgresql import JSON

class Procedure(db.Model):
	__tablename__ = 'procedures'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.String(10))
	procedure_type = db.Column(db.Integer, db.ForeignKey('procedure_types.id'), nullable=False)
	created = db.Column(db.Date, default=db.func.now())
	successful = db.Column(db.Boolean)
	comments = db.Column(db.String(400))

	def __init__(self, user_id, type, created, successful, attempts):
		self.user_id=user_id
		self.procedure_type=type
		self.created=created
		self.successful=successful
		self.attempts=attempts

	def __repr__(self):
		return '<id {}>'.format(self.id)

class ProcedureType(db.Model):
	__tablename__ = 'procedure_types'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(64))
	method_group = db.Column(db.Integer, db.ForeignKey('groups.id'))
	anatomy_group = db.Column(db.Integer, db.ForeignKey('groups.id'))
	show_success = db.Column(db.Boolean)
	weight = db.Column(db.Integer)

	def __repr__(self):
		return '<id {}>'.format(self.id)

class Group(db.Model):
	__tablename__ = 'groups'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(64))

	item = db.relationship('GroupItems', order_by="GroupItems.id", backref="group")

	def __repr__(self):
		return '<id {}>'.format(self.id)

class GroupItems(db.Model):
	__tablename__ = 'group_items'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
	name = db.Column(db.String(64))
	weight = db.Column(db.Integer)

	group = db.relationship("Group", backref=db.backref('items', order_by='weight'))

	def __repr__(self):
		return '<id {}>'.format(self.id)

#class Diagnostic(db.Model):
#	__tablename__ = 'diagnostics'
#
#	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#	patient_visit = db.Column()
#
#class PatientVisit(db.Model):
#	__tablename__ = 'patient_visits'
#	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#	created = db.Column(db.date, default=db.func.now())
#
#	def __init__(self, created):
#		self.created = created
#
#	def __repr__(self):
#		return '<id {}>'.format(self.id)

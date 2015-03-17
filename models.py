from application import db
from sqlalchemy.dialects.postgresql import JSON

"""Procedure class"""
class Procedure(db.Model):
	__tablename__ = 'procedures'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	procedure_type = db.Column(db.Integer, db.ForeignKey('procedure_types.id'), nullable=False)
	method_id = db.Column(db.Integer, db.ForeignKey('group_items.id'), nullable=True)
	anatomy_id = db.Column(db.Integer, db.ForeignKey('group_items.id'), nullable=True)
	tuition = db.Column(db.Boolean, default=False)
	created = db.Column(db.Date, default=db.func.now())
	successful = db.Column(db.Boolean, nullable=True)
	comments = db.Column(db.String(400), nullable=True)

	user = db.relationship("User", foreign_keys=[user_id])
	method = db.relationship("GroupItem", foreign_keys=[method_id])
	anatomy = db.relationship("GroupItem", foreign_keys=[anatomy_id])

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id'				: self.id,
			'procedure_type'	: self.procedure_type,
			'method_id'  		: self.method_id,
			'anatomy_id'		: self.anatomy_id,
			'tuition'			: self.tuition,
			'created'			: str(self.created),
			'successful'		: self.successful,
			'comments'			: self.comments
		}

	def __init__(self, user_id, type, method, anatomy, tuition, created, successful, comments):
		self.user_id=user_id
		self.procedure_type=type
		self.method_id=method
		self.anatomy_id=anatomy
		self.tuition=tuition
		self.created=created
		self.successful=successful
		self.comments=comments

	def __repr__(self):
		return '<id {}>'.format(self.id)

"""Procedure Type class"""
class ProcedureType(db.Model):
	__tablename__ = 'procedure_types'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(64), nullable=False)
	method_group = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
	anatomy_group = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=True)
	show_success = db.Column(db.Boolean, default=False)
	weight = db.Column(db.Integer, nullable=False, default=0)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id'				: self.id,
			'name'				: self.name,
			'method_group'		: self.method_group,
			'anatomy_group'		: self.anatomy_group,
			'show_success'		: self.show_success,
			'weight' 			: self.weight
		}

	def __repr__(self):
		return "<ProcedureType(name=>'%s'" % (self.name)

"""Group class"""
class Group(db.Model):
	__tablename__ = 'groups'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(64), nullable=False)

	items = db.relationship('GroupItem', backref="group")

	def __repr__(self):
		return '<id {}>'.format(self.id)

"""Group Item class"""
class GroupItem(db.Model):
	__tablename__ = 'group_items'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
	name = db.Column(db.String(64), nullable=False)
	weight = db.Column(db.Integer, nullable=False, default=0)

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id'		: self.id,
			'group_id'	: self.group_id,
			'name'  	: self.name,
			'weight'	: self.weight
		}

	def __repr__(self):
		return '<id {}>'.format(self.id)

"""User class"""
class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(32))
	username = db.Column(db.String(32))

	def __repr__(self):
		return '<user {}>'.format(self.id)

"""Patient class"""
class Patient(db.Model):
	__tablename__ = 'patients'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
	age_id = db.Column(db.Integer, db.ForeignKey('group_items.id'), nullable=False)
	triage_id = db.Column(db.Integer, db.ForeignKey('group_items.id'), nullable=False)
	retts_id = db.Column(db.Integer, db.ForeignKey('retts_codes.id'), nullable=True)
	admittance = db.Column(db.Boolean, nullable=True)
	tuition = db.Column(db.Boolean, default=False)
	comments = db.Column(db.String(400))
	created = db.Column(db.Date, default=db.func.now())

	user = db.relationship("User", foreign_keys=[user_id])
	age = db.relationship("GroupItem", foreign_keys=[age_id])
	triage = db.relationship("GroupItem", foreign_keys=[triage_id])
	retts = db.relationship("RettsCode", foreign_keys=[retts_id])

	def __repr__(self):
		return '<patient {}>'.format(self.id)

"""Retts code class"""
class RettsCode(db.Model):
	__tablename__ = 'retts_codes'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(64), nullable=False)
	code = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<RETTS Code {}>'.format(self.id)

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

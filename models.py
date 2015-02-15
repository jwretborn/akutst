from application import db
from sqlalchemy.dialects.postgresql import JSON

class Procedure(db.Model):
	__tablename__ = 'procedures'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.String(10))
	type = db.Column(db.Integer, nullable=False)
	created = db.Column(db.Date, default=db.func.now())
	successful = db.Column(db.Boolean)
	attempts = db.Column(db.SmallInteger)

	def __init__(self, user_id, type, created, successful, attempts):
		self.user_id=user_id, 
		self.type=type, 
		self.created=created, 
		self.successful=successful, 
		self.attempts=attempts

	def __repr__(self):
		return '<id {}>'.format(self.id)
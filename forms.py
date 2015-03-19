
from wtforms import Form, BooleanField, TextField, IntegerField, PasswordField, validators

'''Form class for procedures'''
class ProcedureForm(Form):
	user_id = TextField('ID', [validators.Length(min=2, max=32), validators.Required()])
	procedure = IntegerField('Procedur', [validators.Required()])
	method = IntegerField('Metod')
	anatomy = IntegerField('Lokal')
	tuition = BooleanField('Handledning')
	date = TextField('Datum', [validators.Length(min=10, max=10)])
	successful = BooleanField('Proceduren lyckades')
	comments = TextField('Kommentar', [validators.Length(max=400)])

'''Form class for patientes'''
class PatientForm(Form):
	user_id = TextField('ID', [validators.Length(min=2, max=32), validators.Required()])
	age = IntegerField('Age', [validators.Required()])
	prio = IntegerField('Triage prioritet', [validators.Required()])
	retts = IntegerField('Retts code', [validators.Required()])
	admittance = BooleanField('Inlaggning')
	tuition = BooleanField('Handledning')
	comments = TextField('Kommentar', [validators.Length(max=400)])
	date = TextField('Datum', [validators.Length(min=10, max=10)])

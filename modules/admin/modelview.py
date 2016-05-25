from flask import abort, redirect, request, url_for
from flask_admin.contrib import sqla
from flask_security import login_required, current_user
from sqlalchemy import func
from models import Patient, Procedure


class MyModelView(sqla.ModelView):
	page_size = 20

	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			return False

		if current_user.has_role('superuser'):
			return True

		return False

	def _handle_view(self, name, **kwargs):
		"""
		Override builtin _handle_view in order to redirect users when a view is not accessible.
		"""
		if not self.is_accessible():
			if current_user.is_authenticated:
				# permission denied
				abort(403)
			else:
				# login
				return redirect(url_for('security.login', next=request.url))

class PatientModelView(MyModelView):
	column_searchable_list = ['comments', 'retts.name']
	column_editable_list = ['admittance', 'tuition', 'comments']
	column_filters = ['user.username', 'retts.name']
	can_export = True

	column_select_related_list = ['user', 'retts']

	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			return False

		if current_user.has_role('user') :
			return True
		if current_user.has_role('superuser') :
			return True

		return False

	def get_query(self):
		if current_user.has_role('user') :
			return super(PatientModelView, self).get_query().filter(
				Patient.user_id == current_user.id
			)
		else :
			return super(PatientModelView, self).get_query()

	def get_count_query(self):
		if current_user.has_role('user') :
			return self.session.query(func.count('*')).select_from(self.model).filter(Patient.user_id == current_user.id)
		else :
			return super(PatientModelView, self).get_count_query()

class ProcedureModelView(MyModelView):
	column_searchable_list = ['comments']
	column_filters = ['user.username', 'procedure']
	can_export = True

	column_select_related_list = ['user', 'procedure']

	def is_accessible(self):
		if not current_user.is_active or not current_user.is_authenticated:
			return False

		if current_user.has_role('user') :
			return True
		if current_user.has_role('superuser') :
			return True

		return False

	def get_query(self):
		if current_user.has_role('user') :
			return super(ProcedureModelView, self).get_query().filter(
				Procedure.user_id == current_user.id
			)
		else :
			return super(ProcedureModelView, self).get_query()

	def get_count_query(self):
		if current_user.has_role('user') :
			return self.session.query(func.count('*')).select_from(self.model).filter(Procedure.user_id == current_user.id)
		else :
			return super(ProcedureModelView, self).get_count_query()

class RettsCodeModelView(MyModelView):
	column_searchable_list = ['name', 'code', 'type']
	column_filters = ['type']


class UserModelView(MyModelView):
	column_exclude_list = ['password', ]
	form_excluded_columns = ['password', ]

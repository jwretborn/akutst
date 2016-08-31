from flask_admin import BaseView, expose

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/analytics_index.html')

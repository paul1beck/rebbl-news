from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, request
from flask_login import current_user

class AdminView(ModelView):
    column_exclude_list = ('content')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_folder = 'static'

    def is_accessible(self):
        return current_user.coachname == 'Gypsy Prince'

    def inaccessible_callback(self, name, **kwargs):
        if not self.is_accessible():
            return redirect(url_for('main.home', next=request.url))
        
#    def is_accessible(self):
#        return current_user.role[0] == 'Admin'
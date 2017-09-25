# -*- coding:utf-8 -*-
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import login_required


class CustomView(BaseView):
    
    @expose('/')
    @login_required
    def index(self):
        return self.render('/admin/custom.html')

    @expose('/second_page')
    @login_required
    def second_page(self):
        return self.render('admin/second_page.html')

    
class CustomModelView(ModelView):
    pass


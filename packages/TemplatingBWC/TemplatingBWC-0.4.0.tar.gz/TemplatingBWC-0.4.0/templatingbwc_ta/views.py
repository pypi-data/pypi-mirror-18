from blazeweb.globals import user
from blazeweb.views import View
from blazeweb.utils import redirect

import templatingbwc_ta.forms as forms
import templatingbwc_ta.grids as grids
import templatingbwc_ta.model.orm as orm
from compstack.common.lib.views import CrudBase


class Login(View):
    def default(self):
        user.is_authenticated = True
        user.display_name = 'testuser'
        user.add_message('success', 'You have been logged in.')
        redirect('/')


class Logout(View):
    def default(self):
        user.is_authenticated = False
        user.display_name = None
        user.add_message('success', 'You have been logged out.')
        redirect('/')


class UserMessages(View):
    def default(self):
        types = 'error', 'warning', 'notice', 'success'
        for type in types:
            user.add_message(type, 'This is a %s message.' % type)
        self.render_template()


class Forms(View):
    def default(self):
        self.assign('form1', forms.Make())
        self.assign('form2', forms.Form2())
        self.render_template()


class MakeCrud(CrudBase):

    def init(self):
        CrudBase.init(self, 'Make', 'Makes', forms.Make, orm.Make, gridcls=grids.Make)
        self.allow_anonymous = True
        self.add_processor('option')

    def prep_makes(self):
        count = orm.Make.count()
        if count != 5:
            orm.Make.delete_all()
            orm.Make.add(label=u'Ford')
            orm.Make.add(label=u'Chevy')
            orm.Make.add(label=u'Mercury')
            orm.Make.add(label=u'GMC')
            orm.Make.add(label=u'Honda')

    def auth_post(self, action=None, objid=None, option=None):
        self.option = option
        self.prep_makes()
        CrudBase.auth_post(self, action, objid)

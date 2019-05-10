from flask import Flask, redirect, url_for, request, flash, render_template
from config import Configuration
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from oauth import OAuthSignIn


from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security, current_user

app = Flask(__name__)
app.config.from_object(Configuration)

lm = LoginManager(app)
lm.login_view = 'index'

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

### adminka
from models import *

class AdminMixin:
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('security.login', next=request.url))

class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super(BaseModelView, self).on_model_change(form, model, is_created)

class AdminView(AdminMixin, ModelView):
    pass

class HomeAdminView(AdminMixin, AdminIndexView):
    pass

class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ['title', 'body', 'tags']

class TagAdminView(AdminMixin, BaseModelView):
    pass
    form_columns = ['name', 'posts', 'post_id']

class RoleAdminView(ModelView):
    pass

class UserAdminView(ModelView):
    pass
    # form_columns = ['role_id']


class CommentAdminView(BaseModelView):
    pass
    # form_columns = ['body', 'id']


admin = Admin(app, 'MainPage', url='/', index_view=HomeAdminView(name='home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(RoleAdminView(Role, db.session))
admin.add_view(CommentAdminView(Comment, db.session))

###user manager
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

###oauth
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    roles_users = Role.query.filter_by(id='1').first()
    print(roles_users)
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        # user.roles_users.append(user.id, '1')

        user = User(social_id=social_id, nickname=username, email=email)
        # print('asdasdasd', user)
        db.session.add(user)
        db.session.commit()
        print(user.id)
        # roles_users = Role.query.filter_by(id='1').first()
        # print(roles_users)
        # roles_users = roles_users(user.id, roles_users)
        # user.roles_users.append(1)
        # print('asdasdasd', user)
        print(roles_users)
        # db.session.add(roles_users)
        # db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


















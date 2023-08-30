from  flask import Flask, json, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import openai as oa


db = SQLAlchemy()
DB_NAME="dabase.db"


def create_app():
    app = Flask(__name__)
    oa.api_key=""
    app.config["SECRET_KEY"]= "benjidevpythontime"
    app.config["SQLALCHEMY_DATABASE_URI"]=f'sqlite:///{DB_NAME}'
    db.init_app(app)



    from .views import views
    from .auth import auth


    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix="/")


    from .models import User, Note

    with app.app_context():
        db.create_all()
        print('Created Db!')

    login_manager = LoginManager()
    login_manager.login_view= 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    return app

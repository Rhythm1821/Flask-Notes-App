from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager,current_user

db = SQLAlchemy()
DB_NAME = 'database.db'



def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'efudnjkeu23'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from website.views import views
    from website.auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    from website.models import User,Note
    with app.app_context():
        create_database()

    # To redirect user to login page if not logged in 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app


def create_database():
    if not path.exists(DB_NAME):
        db.create_all()
        print('Database Created')
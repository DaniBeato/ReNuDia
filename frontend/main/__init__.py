import os
from flask import Flask
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_login import LoginManager

csrf = CSRFProtect()
login_manager = LoginManager()




def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    csrf.init_app(app)
    app.config["WTF_CSRF_TIME_LIMIT"] = None
    login_manager.init_app(app)
    from main.routes import main
    app.register_blueprint(routes.main.main)
    from main.routes import nutritional_record
    app.register_blueprint(routes.nutritional_record.nutritional_record)
    from main.routes import message
    app.register_blueprint(routes.message.message)
    from main.routes import inscription
    app.register_blueprint(routes.inscription.inscription)
    from main.routes import food
    app.register_blueprint(routes.food.food)
    return app
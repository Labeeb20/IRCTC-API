from flask import Flask
from models import db
from config import Config
from flask_jwt_extended import JWTManager
from routes import app as routes_app

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)


# Initialize routes
app.register_blueprint(routes_app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

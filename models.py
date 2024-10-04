from flask_sqlalchemy import SQLAlchemy
import uuid;

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default='user')

    def __init__(self, username, email, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password

class Train(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    train_name = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)

    def __init__(self, train_name, source, destination, total_seats):
        self.id = str(uuid.uuid4())
        self.train_name = train_name
        self.source = source
        self.destination = destination
        self.total_seats = total_seats
        self.available_seats = total_seats

class Booking(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    seat_count = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    train_id = db.Column(db.String(36), db.ForeignKey('train.id'))

    def __init__(self, seat_count, user_id, train_id):
        self.id = str(uuid.uuid4())
        self.seat_count = seat_count
        self.user_id = user_id
        self.train_id = train_id

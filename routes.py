from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from models import db, User, Train, Booking

app = Blueprint('app', __name__)
bcrypt = Bcrypt()
jwt = JWTManager()

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/trains', methods=['POST'])
@jwt_required()
def add_train():
    data = request.get_json()
    new_train = Train(train_name=data['train_name'], source=data['source'], destination=data['destination'], total_seats=data['total_seats'])
    db.session.add(new_train)
    db.session.commit()
    
    return jsonify({'message': 'Train added successfully'}), 201

@app.route('/trains/availability', methods=['GET'])
def get_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    trains = Train.query.filter_by(source=source, destination=destination).all()
    return jsonify([{
        'train_name': train.train_name,
        'available_seats': train.available_seats
    } for train in trains]), 200

@app.route('/book', methods=['POST'])
@jwt_required()
def book_seat():
    data = request.get_json()
    train_id = data['train_id']
    seat_count = data['seat_count']

    train = Train.query.get(train_id)
    if not train or train.available_seats < seat_count:
        return jsonify({'message': 'Not enough seats available'}), 400

    train.available_seats -= seat_count
    new_booking = Booking(seat_count=seat_count, user_id=data['user_id'], train_id=train_id)

    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({'message': 'Booking successful'}), 200


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://my_username:my_password@localhost:5432/my_phase5backend'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(15))
    location = db.Column(db.Text)
    role = db.Column(db.String(10), default='buyer')

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    images = db.Column(db.ARRAY(db.String), nullable=True)
    farmer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='available')

# Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        name=data['name'],
        email=data['email'],
        password_hash=hashed_password,
        phone=data['phone'],
        location=data['location'],
        role=data.get('role', 'buyer')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity={
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role
    })
    return jsonify({'access_token': access_token, 'user': {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'role': user.role
    }}), 200

@app.route('/api/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response, 200

@app.route('/api/animals', methods=['POST'])
@jwt_required()
def create_animal():
    data = request.form
    images = request.files.getlist('images')

    if not data or not images:
        return jsonify({'message': 'Missing data or images'}), 400

    user_id = get_jwt_identity()['id']
    animal = Animal(
        type=data['type'],
        breed=data['breed'],
        age=int(data['age']),
        price=float(data['price']),
        description=data['description'],
        farmer_id=user_id
    )

    image_urls = []
    for image in images:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)
        image_urls.append(image_path)

    animal.images = image_urls
    db.session.add(animal)
    db.session.commit()

    return jsonify({'message': 'Animal created successfully', 'animal': animal.id}), 201

@app.route('/api/animals/<int:animal_id>', methods=['PUT'])
@jwt_required()
def update_animal(animal_id):
    data = request.form
    images = request.files.getlist('images')

    if not data:
        return jsonify({'message': 'Missing data'}), 400

    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({'message': 'Animal not found'}), 404

    user_id = get_jwt_identity()['id']
    if animal.farmer_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    animal.type = data['type']
    animal.breed = data['breed']
    animal.age = int(data['age'])
    animal.price = float(data['price'])
    animal.description = data['description']

    if images:
        image_urls = []
        for image in images:
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            image_urls.append(image_path)
        animal.images = image_urls

    db.session.commit()

    return jsonify({'message': 'Animal updated successfully', 'animal': animal.id}), 200

@app.route('/api/animals/<int:animal_id>', methods=['DELETE'])
@jwt_required()
def delete_animal(animal_id):
    animal = Animal.query.get(animal_id)
    if not animal:
        return jsonify({'message': 'Animal not found'}), 404

    user_id = get_jwt_identity()['id']
    if animal.farmer_id != user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(animal)
    db.session.commit()

    return jsonify({'message': 'Animal deleted successfully'}), 200

@app.route('/api/animals', methods=['GET'])
@jwt_required()
def get_animals():
    user_id = get_jwt_identity()['id']
    animals = Animal.query.filter_by(farmer_id=user_id).all()

    return jsonify([{
        'id': animal.id,
        'type': animal.type,
        'breed': animal.breed,
        'age': animal.age,
        'price': animal.price,
        'description': animal.description,
        'images': animal.images,
        'status': animal.status
    } for animal in animals]), 200

# Start Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

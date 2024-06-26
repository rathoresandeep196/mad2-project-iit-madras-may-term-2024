from flask import Flask, jsonify, render_template_string, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from datetime import timedelta, datetime
from werkzeug.utils import secure_filename

from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

from flask_caching import Cache

from worker import celery_init_app
from tasks import celery_test
from celery.result import AsyncResult


# from celery import Celery





app = Flask(__name__)


# app = Celery('main', broker='redis://localhost:6379/0')

# # Load tasks from all modules named 'tasks' within the current directory
# app.autodiscover_tasks(['main'])


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///librarymanagement.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'  # or the hostname of your Redis server
app.config['CACHE_REDIS_PORT'] = 6379        # or the port number of your Redis server
app.config['CACHE_REDIS_DB'] = 0              # the database number (0 by default)
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'  # alternative way to set Redis URL

# Initialize the cache
cache = Cache(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)
celery_app=celery_init_app(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class BookSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(150), nullable=False)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(150), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('book_section.id'), nullable=False)

    # def __init__(self, title, date_created, description, file_path):
    #     self.title = title
    #     self.date_created = date_created
    #     self.description = description
    #     self.file_path = file_path

@app.route('/cache-test')
@cache.cached(timeout=10)
def cache():
    date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return render_template_string('{{ date }}', date=date)


# Routes
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email already exists'}), 400

    new_user = User(
        first_name=data['firstName'],
        last_name=data['lastName'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        role=data['role']
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid email or password'}), 401

    user_info = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.role
    }

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))

    return jsonify({'access_token': access_token, 'role': user.role, 'user_info': user_info}), 200

@app.route('/api/search/user', methods=['GET'])
@jwt_required()
def search_user():
    first_name = request.args.get('first_name')
    if not first_name:
        return jsonify({'message': 'First name parameter is required'}), 400

    users = User.query.filter(User.first_name.ilike(f'%{first_name}%')).all()
    if not users:
        return jsonify({'message': 'No users found'}), 404

    user_list = [{'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'role': user.role} for user in users]

    return jsonify({'users': user_list}), 200

# @app.route('/add-section', methods=['POST'])
# @jwt_required()
# def add_section():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part in the request"}), 400

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No file selected for uploading"}), 400

#     if file:
#         # filename = secure_filename(file.filename)
#         # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

#         file.save('./static/'+'one.pdf')

#         new_section = BookSection(
#             title=request.form['title'],
#             date_created=datetime.strptime(request.form['dateCreated'], '%Y-%m-%d'),
#             description=request.form['description'],
#             file_path='./static/'+'one.pdf' # change this
#         )

#         db.session.add(new_section)
#         db.session.commit()

#         return jsonify({"message": "Book section added successfully"}), 201

#     return jsonify({"error": "Failed to add book section"}), 500


@app.route('/add-section', methods=['POST'])
@jwt_required()
def add_section():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        # First, create the section without the file path
        new_section = BookSection(
            title=request.form['title'],
            date_created=datetime.strptime(request.form['dateCreated'], '%Y-%m-%d'),
            description=request.form['description'],
            file_path=''  # Temporary file path
        )

        db.session.add(new_section)
        db.session.commit()

        # Generate the file path using the section ID
        filename = f"{new_section.id}.pdf"
        static_folder = os.path.join(os.getcwd(), 'static')  # Define the static folder path
        file_path = os.path.join(static_folder, filename)

        # Ensure the static folder exists
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        # Save the file
        file.save(file_path)

        # Update the section with the correct file path
        new_section.file_path = file_path
        db.session.commit()

        return jsonify({"message": "Book section added successfully"}), 201

    return jsonify({"error": "Failed to add book section"}), 500



@app.route('/sections', methods=['GET'])
def get_sections():
    sections = BookSection.query.all()
    return jsonify([{
        'id': section.id,
        'title': section.title,
        'date_created': section.date_created,
        'description': section.description,
        'file_path': section.file_path
    } for section in sections])

@app.route('/section/<int:id>', methods=['GET'])
def get_section(id):
    section = BookSection.query.get_or_404(id)
    return jsonify({
        'id': section.id,
        'title': section.title,
        'date_created': section.date_created,
        'description': section.description,
        'file_path': section.file_path
    })

@app.route('/section/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_section(id):
    section = BookSection.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "Section deleted successfully"}), 200

@app.route('/edit-section/<int:id>', methods=['PUT'])
@jwt_required()
def edit_section(id):
    section = BookSection.query.get_or_404(id)
    section.title = request.form['title']
    section.date_created = datetime.strptime(request.form['dateCreated'], '%Y-%m-%d')
    section.description = request.form['description']

    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            section.file_path = file_path

    db.session.commit()
    return jsonify({"message": "Section updated successfully"}), 200


@app.route('/add-book', methods=['POST'])
@jwt_required()
def add_book():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        # First, create the book entry without the file path
        try:
            date_created = datetime.strptime(request.form['dateCreated'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid date format, should be YYYY-MM-DD"}), 400
        
        new_book = Book(
            title=request.form['title'],
            date_created=date_created,
            description=request.form['description'],
            file_path='',  # Temporary file path
            section_id=request.form['section_id']
        )

        db.session.add(new_book)
        db.session.commit()

        # Generate the file path using the book ID
        filename = f"{new_book.id}.pdf"
        book_folder = os.path.join(os.getcwd(), 'assets')  # Define the Book folder path
        file_path = os.path.join(book_folder, filename)

        # Ensure the Book folder exists
        if not os.path.exists(book_folder):
            os.makedirs(book_folder)

        # Save the file
        file.save(file_path)

        # Update the book with the correct file path
        new_book.file_path = file_path
        db.session.commit()

        return jsonify({"message": "Book added successfully"}), 201

    return jsonify({"error": "Failed to add book"}), 500

@app.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'date_created': book.date_created.strftime('%Y-%m-%d'),
            'description': book.description,
            'file_path': book.file_path,
            'section_id': book.section_id
        }
        book_list.append(book_data)
    return jsonify({'books': book_list})

@app.route('/book/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get_or_404(id)

    try:
        # Delete the file associated with the book
        if os.path.exists(book.file_path):
            os.remove(book.file_path)

        db.session.delete(book)
        db.session.commit()

        return jsonify({"message": "Book deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete book: {str(e)}"}), 500
    

@app.route('/assets/<filename>')
def download_file(filename):
    print(filename)
    return send_from_directory('assets/', filename)




@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    return jsonify({'message': 'Logout successful'}), 200

@app.route("/")
def hello():
    return "Hello World!"



#### ------------------ celery TEST ------------------ ####

@app.route('/celery/test')
def celery_test_endpoint():
    result = celery_test.delay(5,6)

    return str(result)

@app.route('/celery/status/<task_id>')
def celery_status_endpoint(task_id):
    result = AsyncResult(task_id)

    return str(result.result)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

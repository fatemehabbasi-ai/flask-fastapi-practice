from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = generate_password_hash(data["password"])
    new_user = User(username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"status": "success", "message": "User registered!"}),201
        
@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = [{"id": u.id, "username": u.username, "password": u.password} for u in all_users]
    return jsonify(result)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.json
        username = data["username"]
        password = data["password"]
        user=User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            return jsonify({"status": "success", "message": "Login successful!"}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401
    else:
        return jsonify({"status": "Try again", "message": "Please send a POST request to login."})
        
    

@app.route("/")
def say_hello():
    return("Hello!")

@app.route("/greet/<name>")
def greet_use(name):
    return f"Hello, {name}!"

@app.route("/age/<int:age>")
def age_user(age):
    age = 100 - age
    return f"You will turn 100 in {age} years!"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
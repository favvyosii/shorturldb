from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random, string

app = Flask(__name__)
CORS(app)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# URL model
class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(10), nullable=False, unique=True)

# Generate random short URL
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# API endpoint to shorten a URL
@app.route("/")
def home():
    return "Hello from home route"
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.json
    original_url = data.get('url')
    
    if original_url:
        short_url = generate_short_url()
        url_entry = URL(original_url=original_url, short_url=short_url)
        db.session.add(url_entry)
        db.session.commit()
        
        # return jsonify({'short_url': f"http://localhost:5000/{short_url}"})
        return jsonify({'short_url': f"https://shorturldb.onrender.com/{short_url}"})

    
    return jsonify({'error': 'Invalid URL'}), 400

# API endpoint to redirect to the original URL
@app.route('/<short_url>', methods=['GET'])
def redirect_to_url(short_url):
    url_entry = URL.query.filter_by(short_url=short_url).first()
    
    if url_entry:
        return redirect(url_entry.original_url)
    
    return jsonify({'error': 'URL not found'}), 404

if __name__ == "__main__":
    # Ensure the app context is available when creating the database
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)

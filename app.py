import os
import base64
import logging
import uuid
from urllib.parse import quote

from flask import Flask, render_template, request, jsonify, session

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "test_secret_key")

# In-memory storage for users
users = {}

@app.route('/')
def home():
    """Home page endpoint that displays welcome message and user details if available."""
    return render_template('index.html', users=users)

@app.route('/submit', methods=['POST'])
def submit():
    """
    Endpoint to submit user information.
    Accepts POST requests with name and email parameters.
    Returns a JSON response with user_id and confirmation message.
    """
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        
        # Validate input
        if not name or not email:
            return jsonify({
                'error': 'Name and email are required'
            }), 400
            
        # Generate a unique user ID
        user_id = str(uuid.uuid4())
        
        # Store user data
        users[user_id] = {
            'name': name,
            'email': email,
            'id': user_id
        }
        
        logger.debug(f"Created user: {users[user_id]}")
        
        return jsonify({
            'user_id': user_id,
            'message': f'User {name} with email {email} has been registered'
        })
    except Exception as e:
        logger.error(f"Error in submit endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500

@app.route('/user', methods=['GET'])
def get_user():
    """
    Endpoint to get user information.
    Accepts GET requests with user_id parameter.
    Returns user information as JSON.
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({
                'error': 'user_id parameter is required'
            }), 400
            
        user = users.get(user_id)
        
        if not user:
            return jsonify({
                'error': f'User with ID {user_id} not found'
            }), 404
            
        return jsonify(user)
    except Exception as e:
        logger.error(f"Error in get_user endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500

@app.route('/encode', methods=['POST'])
def encode_message():
    """
    Endpoint to encode a message in various formats.
    Accepts POST requests with a message parameter.
    Returns the message encoded in base64, hex, and URL-encoded formats.
    """
    try:
        message = request.form.get('message', '')
        
        if not message:
            return jsonify({
                'error': 'message parameter is required'
            }), 400
            
        # Encode the message in various formats
        base64_encoded = base64.b64encode(message.encode()).decode()
        hex_encoded = message.encode().hex()
        url_encoded = quote(message)
        
        return jsonify({
            'original': message,
            'base64': base64_encoded,
            'hex': hex_encoded,
            'url_encoded': url_encoded
        })
    except Exception as e:
        logger.error(f"Error in encode_message endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configuration
from config import config
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# CORS
CORS(app, resources={
    r"/api/*": {
        "origins": app.config['CORS_ORIGINS'],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize database
from app.models.database import Database
app.db = Database(app.config['DATABASE_PATH'])
print(f"✓ Database initialized: {app.config['DATABASE_PATH']}")

# Register blueprints
from app.routes.transactions import transactions_bp
from app.routes.chat import chat_bp

app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
app.register_blueprint(chat_bp, url_prefix='/api/chat')

# Health check
@app.route('/health')
def health():
    return {'status': 'healthy'}

@app.route('/')
def index():
    return {
        'message': 'Student Finance AI API',
        'endpoints': {
            'transactions': '/api/transactions',
            'chat': '/api/chat',
            'health': '/health'
        }
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"\n{'='*50}")
    print(f"Starting Flask Server")
    print(f"{'='*50}")
    print(f"Environment: {config_name}")
    print(f"URL: http://{host}:{port}")
    print(f"Database: {app.config['DATABASE_PATH']}")
    print(f"{'='*50}\n")
    
    app.run(host=host, port=port, debug=app.config['DEBUG'])

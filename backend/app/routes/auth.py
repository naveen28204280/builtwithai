from flask import Blueprint, request, jsonify, current_app
import sqlite3
from datetime import datetime
import hashlib

auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    """Simple password hashing (use bcrypt in production)"""
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.json
    
    if not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'username, email, and password required'}), 400
    
    try:
        conn = current_app.db.get_connection()
        cursor = conn.cursor()
        
        # Hash password
        password_hash = hash_password(data['password'])
        
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (data['username'], data['email'], password_hash))
        
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'user_id': user_id,
            'username': data['username'],
            'email': data['email'],
            'message': 'User registered successfully'
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'username and password required'}), 400
    
    try:
        conn = current_app.db.get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(data['password'])
        
        cursor.execute('''
            SELECT id, username, email, created_at 
            FROM users 
            WHERE username = ? AND password_hash = ?
        ''', (data['username'], password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        return jsonify({
            'user_id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at'],
            'message': 'Login successful'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user info by ID"""
    try:
        conn = current_app.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, email, created_at 
            FROM users 
            WHERE id = ?
        ''', (user_id,))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/users', methods=['GET'])
def list_users():
    """List all users"""
    try:
        conn = current_app.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, email, created_at FROM users')
        users = cursor.fetchall()
        conn.close()
        
        return jsonify([{
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at']
        } for user in users]), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

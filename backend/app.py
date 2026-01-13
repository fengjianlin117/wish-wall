from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///wish_wall.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# ==================== Database Models ====================

class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120))
    avatar_url = db.Column(db.String(255))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    wishes = db.relationship('Wish', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_email=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'display_name': self.display_name,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'created_at': self.created_at.isoformat(),
            'wishes_count': len(self.wishes),
        }
        if include_email:
            data['email'] = self.email
        return data


class Wish(db.Model):
    """Wish model for storing user wishes"""
    __tablename__ = 'wishes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='general')
    image_url = db.Column(db.String(255))
    is_public = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), default='active')  # active, completed, archived
    priority = db.Column(db.Integer, default=0)  # 0=low, 1=medium, 2=high
    target_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='wish', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='wish', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_author=True, include_comments=False):
        """Convert wish to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'image_url': self.image_url,
            'is_public': self.is_public,
            'status': self.status,
            'priority': self.priority,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'likes_count': len(self.likes),
            'comments_count': len(self.comments),
        }
        if include_author:
            data['author'] = self.author.to_dict()
        if include_comments:
            data['comments'] = [comment.to_dict() for comment in self.comments]
        return data


class Comment(db.Model):
    """Comment model for wish comments/encouragement"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    wish_id = db.Column(db.Integer, db.ForeignKey('wishes.id'), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert comment to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'author': self.author.to_dict(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }


class Like(db.Model):
    """Like model for wish likes"""
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    wish_id = db.Column(db.Integer, db.ForeignKey('wishes.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'wish_id', name='unique_like'),)
    
    def to_dict(self):
        """Convert like to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'wish_id': self.wish_id,
            'created_at': self.created_at.isoformat(),
        }


# ==================== Authentication Endpoints ====================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409
    
    try:
        user = User(
            username=data['username'],
            email=data['email'],
            display_name=data.get('display_name', data['username'])
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user.to_dict(include_email=True),
            'access_token': access_token
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(include_email=True),
        'access_token': access_token
    }), 200


@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict(include_email=True)), 200


@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """Refresh access token"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200


# ==================== User Endpoints ====================

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile by ID"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user profile"""
    current_user_id = get_jwt_identity()
    
    if current_user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'display_name' in data:
        user.display_name = data['display_name']
    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url']
    if 'bio' in data:
        user.bio = data['bio']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict(include_email=True)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/users/<int:user_id>/wishes', methods=['GET'])
def get_user_wishes(user_id):
    """Get all wishes by a user"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    wishes = Wish.query.filter_by(user_id=user_id, is_public=True).order_by(Wish.created_at.desc()).all()
    
    return jsonify({
        'user': user.to_dict(),
        'wishes': [wish.to_dict() for wish in wishes]
    }), 200


# ==================== Wish Endpoints ====================

@app.route('/api/wishes', methods=['GET'])
def get_wishes():
    """Get all public wishes with pagination and filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category = request.args.get('category')
    status = request.args.get('status', 'active')
    sort_by = request.args.get('sort_by', 'created_at')
    
    query = Wish.query.filter_by(is_public=True)
    
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    
    if sort_by == 'likes':
        query = query.outerjoin(Like).group_by(Wish.id).order_by(db.func.count(Like.id).desc())
    elif sort_by == 'comments':
        query = query.outerjoin(Comment).group_by(Wish.id).order_by(db.func.count(Comment.id).desc())
    else:
        query = query.order_by(Wish.created_at.desc())
    
    pagination = query.paginate(page=page, per_page=per_page)
    
    return jsonify({
        'wishes': [wish.to_dict() for wish in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200


@app.route('/api/wishes', methods=['POST'])
@jwt_required()
def create_wish():
    """Create a new wish"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Missing required fields (title, content)'}), 400
    
    try:
        wish = Wish(
            user_id=user_id,
            title=data['title'],
            content=data['content'],
            category=data.get('category', 'general'),
            image_url=data.get('image_url'),
            is_public=data.get('is_public', True),
            priority=data.get('priority', 0),
            target_date=datetime.fromisoformat(data['target_date']) if data.get('target_date') else None
        )
        
        db.session.add(wish)
        db.session.commit()
        
        return jsonify({
            'message': 'Wish created successfully',
            'wish': wish.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/wishes/<int:wish_id>', methods=['GET'])
def get_wish(wish_id):
    """Get a single wish by ID"""
    wish = Wish.query.get(wish_id)
    
    if not wish or (not wish.is_public):
        return jsonify({'error': 'Wish not found'}), 404
    
    return jsonify(wish.to_dict(include_comments=True)), 200


@app.route('/api/wishes/<int:wish_id>', methods=['PUT'])
@jwt_required()
def update_wish(wish_id):
    """Update a wish"""
    user_id = get_jwt_identity()
    wish = Wish.query.get(wish_id)
    
    if not wish:
        return jsonify({'error': 'Wish not found'}), 404
    
    if wish.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if 'title' in data:
        wish.title = data['title']
    if 'content' in data:
        wish.content = data['content']
    if 'category' in data:
        wish.category = data['category']
    if 'image_url' in data:
        wish.image_url = data['image_url']
    if 'is_public' in data:
        wish.is_public = data['is_public']
    if 'status' in data:
        wish.status = data['status']
    if 'priority' in data:
        wish.priority = data['priority']
    if 'target_date' in data:
        wish.target_date = datetime.fromisoformat(data['target_date']) if data['target_date'] else None
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Wish updated successfully',
            'wish': wish.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/wishes/<int:wish_id>', methods=['DELETE'])
@jwt_required()
def delete_wish(wish_id):
    """Delete a wish"""
    user_id = get_jwt_identity()
    wish = Wish.query.get(wish_id)
    
    if not wish:
        return jsonify({'error': 'Wish not found'}), 404
    
    if wish.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(wish)
        db.session.commit()
        return jsonify({'message': 'Wish deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== Comment Endpoints ====================

@app.route('/api/wishes/<int:wish_id>/comments', methods=['GET'])
def get_comments(wish_id):
    """Get all comments for a wish"""
    wish = Wish.query.get(wish_id)
    
    if not wish:
        return jsonify({'error': 'Wish not found'}), 404
    
    comments = Comment.query.filter_by(wish_id=wish_id).order_by(Comment.created_at.desc()).all()
    
    return jsonify({
        'wish_id': wish_id,
        'comments': [comment.to_dict() for comment in comments]
    }), 200


@app.route('/api/wishes/<int:wish_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(wish_id):
    """Add a comment to a wish"""
    user_id = get_jwt_identity()
    wish = Wish.query.get(wish_id)
    
    if not wish:
        return jsonify({'error': 'Wish not found'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Missing content'}), 400
    
    try:
        comment = Comment(
            user_id=user_id,
            wish_id=wish_id,
            content=data['content']
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': comment.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
@jwt_required()
def update_comment(comment_id):
    """Update a comment"""
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    if comment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'error': 'Missing content'}), 400
    
    comment.content = data['content']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Comment updated successfully',
            'comment': comment.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@jwt_required()
def delete_comment(comment_id):
    """Delete a comment"""
    user_id = get_jwt_identity()
    comment = Comment.query.get(comment_id)
    
    if not comment:
        return jsonify({'error': 'Comment not found'}), 404
    
    if comment.user_id != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'message': 'Comment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== Like Endpoints ====================

@app.route('/api/wishes/<int:wish_id>/like', methods=['POST'])
@jwt_required()
def like_wish(wish_id):
    """Like a wish"""
    user_id = get_jwt_identity()
    wish = Wish.query.get(wish_id)
    
    if not wish:
        return jsonify({'error': 'Wish not found'}), 404
    
    existing_like = Like.query.filter_by(user_id=user_id, wish_id=wish_id).first()
    
    if existing_like:
        return jsonify({'error': 'Already liked'}), 400
    
    try:
        like = Like(user_id=user_id, wish_id=wish_id)
        db.session.add(like)
        db.session.commit()
        
        return jsonify({
            'message': 'Wish liked successfully',
            'like': like.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/wishes/<int:wish_id>/unlike', methods=['POST'])
@jwt_required()
def unlike_wish(wish_id):
    """Unlike a wish"""
    user_id = get_jwt_identity()
    
    like = Like.query.filter_by(user_id=user_id, wish_id=wish_id).first()
    
    if not like:
        return jsonify({'error': 'Not liked'}), 404
    
    try:
        db.session.delete(like)
        db.session.commit()
        
        return jsonify({'message': 'Wish unliked successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/wishes/<int:wish_id>/likes', methods=['GET'])
def get_wish_likes(wish_id):
    """Get all likes for a wish"""
    wish = Wish.query.get(wish_id)
    
    if not wish:
        return jsonify({'error': 'Wish not found'}), 404
    
    likes = Like.query.filter_by(wish_id=wish_id).all()
    
    return jsonify({
        'wish_id': wish_id,
        'likes': [like.to_dict() for like in likes],
        'total': len(likes)
    }), 200


# ==================== Stats & Search Endpoints ====================

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get general statistics"""
    total_users = User.query.count()
    total_wishes = Wish.query.filter_by(is_public=True).count()
    total_comments = Comment.query.count()
    total_likes = Like.query.count()
    
    return jsonify({
        'total_users': total_users,
        'total_wishes': total_wishes,
        'total_comments': total_comments,
        'total_likes': total_likes
    }), 200


@app.route('/api/search', methods=['GET'])
def search():
    """Search wishes by title or content"""
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    if not query or len(query) < 2:
        return jsonify({'error': 'Query must be at least 2 characters'}), 400
    
    wishes = Wish.query.filter(
        Wish.is_public == True,
        (Wish.title.ilike(f'%{query}%') | Wish.content.ilike(f'%{query}%'))
    ).order_by(Wish.created_at.desc()).paginate(page=page, per_page=per_page)
    
    return jsonify({
        'query': query,
        'wishes': [wish.to_dict() for wish in wishes.items],
        'total': wishes.total,
        'pages': wishes.pages,
        'current_page': page
    }), 200


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# ==================== Health Check ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


# ==================== Database Initialization ====================

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized successfully')


@app.cli.command()
def seed_db():
    """Seed the database with sample data"""
    # Check if data already exists
    if User.query.first():
        print('Database already has data')
        return
    
    # Create sample users
    user1 = User(
        username='john_doe',
        email='john@example.com',
        display_name='John Doe',
        bio='Dream chaser and wish maker'
    )
    user1.set_password('password123')
    
    user2 = User(
        username='jane_smith',
        email='jane@example.com',
        display_name='Jane Smith',
        bio='Making dreams come true'
    )
    user2.set_password('password123')
    
    db.session.add_all([user1, user2])
    db.session.commit()
    
    # Create sample wishes
    wish1 = Wish(
        user_id=user1.id,
        title='Learn to play guitar',
        content='I want to learn how to play acoustic guitar and play some classics',
        category='hobby',
        priority=2,
        target_date=datetime.utcnow() + timedelta(days=180)
    )
    
    wish2 = Wish(
        user_id=user2.id,
        title='Travel to Japan',
        content='Experience Japanese culture and visit Tokyo, Kyoto, and Mount Fuji',
        category='travel',
        priority=1,
        target_date=datetime.utcnow() + timedelta(days=365)
    )
    
    db.session.add_all([wish1, wish2])
    db.session.commit()
    
    print('Database seeded successfully')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ENUM  # Import ENUM for PostgreSQL
from datetime import datetime

from flask_login import UserMixin  
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db

class User(UserMixin):  

    
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))  

    role = db.Column(ENUM('admin', 'sponsor', 'influencer', name='user_roles', create_type=False), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,onupdate=datetime.utcnow) 
    last_login = db.Column(db.DateTime, nullable=True)

    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    ad_requests = db.relationship('AdRequest', backref='influencer', lazy=True)

    # Password Hashing and Verification
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  

        return check_password_hash(self.password_hash, password)  


    # Dictionary Representation (for API responses)
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() + 'Z', 
            'updated_at': self.updated_at.isoformat() + 'Z',
            'categories': [category.to_dict() for category in self.categories] 

        }


def load_user(user_id):
    from app import login_manager
    return User.query.get(int(user_id))

class Campaign(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Numeric(10, 2))  # (precision, scale) for decimal

    # Use ENUM for visibility (if using PostgreSQL)
    visibility = db.Column(ENUM('public', 'private', name='campaign_visibility', create_type=False), default='public') 
    goals = db.Column(db.Text)

    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    ad_requests = db.relationship('AdRequest', backref='campaign', lazy=True)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.strftime('%Y-%m-%d')  
            if self.start_date else None,
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,  

            'budget': float(self.budget),  # Convert Decimal to float for JSON serialization
            'visibility': self.visibility,
            'goals': self.goals,
            'sponsor_id': self.sponsor_id,
            'sponsor': self.sponsor.to_dict(),  # Include sponsor information
            'categories': [category.to_dict() for category in self.categories]  # Include categories
        }

class AdRequest(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Numeric(10, 2))

    # Use ENUM for status (if using PostgreSQL)
    status = db.Column(ENUM('pending', 'accepted', 'rejected', 'negotiating', name='ad_request_status', create_type=False), default='pending') 

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    def to_dict(self):
        return {
            'id': self.id,
            'campaign_id': self.campaign_id,
            'campaign_name': self.campaign.name,  # Include campaign name
            'influencer_id': self.influencer_id,
            'influencer_username': self.influencer.username,  # Include influencer username
            'message': self.message,
            'requirements': self.requirements,
            'payment_amount': float(self.payment_amount), 
            'status': self.status,
            'created_at': self.created_at.isoformat() + 'Z',
            'updated_at': self.updated_at.isoformat() + 'Z'
        }
class Report(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    report_data = db.Column(db.JSON)  # Store report data in JSON format
    created_at = db.Column(db.DateTime, default=db.func.now())
    
    def to_dict(self):
            return {
                'id': self.id,
                'sponsor_id': self.sponsor_id,
                'start_date': self.start_date.strftime('%Y-%m-%d'),
                'end_date': self.end_date.strftime('%Y-%m-%d'),
                'report_data': self.report_data,
                'created_at': self.created_at.isoformat() + 'Z'}
categories = db.Table('categories',
        db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True),
        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))
class Category(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)

    # Relationships
    campaigns = db.relationship('Campaign', secondary=categories, lazy='subquery',
        backref=db.backref('categories', lazy=True))
    influencers = db.relationship('User', secondary=categories, lazy='subquery',
        backref=db.backref('categories', lazy=True))
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
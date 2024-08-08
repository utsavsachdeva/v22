from flask import Blueprint, request, jsonify,send_file
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash 
from app.utils import is_admin

from flask import current_app

import os

from app.database import db


import os
api = Blueprint('api', __name__)
# Registration Route

@api.route('/')
def index():
    return jsonify({'message': 'Welcome to the Influencer Platform API!'})

@api.route('/register', methods=['POST'])
def register():
    from app.models import User
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Input validation (add more checks as needed)
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username, email, or password'}), 400

    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Username or email already exists'}), 409

    # Create a new user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])  # Hash the password
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# Login Route
@api.route('/login', methods=['POST'])
def login():
    from app.models import User
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200


# Logout Route
@api.route('/logout', methods=['POST'])
@jwt_required() # Requires a valid JWT token for this route
def logout():
    # Invalidate the token on the client-side (frontend responsibility)
    return jsonify({"message": "Logout successful"}), 200



# Get User Details (For admins or the user themselves)
@api.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    from app.models import User
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(id)

    if current_user_id != id and current_user_id != 1:  # Allow admins (id=1)
        return jsonify({'message': 'Unauthorized'}), 403

    return jsonify(user.to_dict()), 200

# Update User Profile (For admins or the user themselves)
@api.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    from app.models import User
    current_user_id = get_jwt_identity()
    user = User.query.get_or_404(id)

    if current_user_id != id and current_user_id != 1:  # Allow admins (id=1)
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Update user fields (add more fields as needed)
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    # ... (update other fields)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200


# Activate/Deactivate User (For admins only)
@api.route('/users/<int:id>/activate', methods=['PUT'])
@jwt_required()
def activate_user(id):
    from app.models import User
    current_user_id = get_jwt_identity()

    if current_user_id != 1:  # Only allow admins
        return jsonify({'message': 'Unauthorized'}), 403

    user = User.query.get_or_404(id)
    user.is_active = not user.is_active  # Toggle active status
    db.session.commit()

    action = 'activated' if user.is_active else 'deactivated'
    return jsonify({'message': f'User {action} successfully'}), 200






# Get All Users (For admins only)
@api.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    from app.models import User
    current_user_id = get_jwt_identity()

    if current_user_id != 1:  # Only allow admins
        return jsonify({'message': 'Unauthorized'}), 403

    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


# Get User Profile
@api.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    from app.models import User
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.to_dict()), 200


# Update User Profile
@api.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    from app.models import User
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Update user fields (add more fields and validation as needed)
    if 'username' in data:
        # Validate username (e.g., check for uniqueness, length, allowed characters)
        if User.query.filter_by(username=data['username']).first() and data['username'] != user.username:
            return jsonify({'message': 'Username already exists'}), 409
        user.username = data['username']
    if 'email' in data:
        # Validate email (e.g., check for uniqueness, format)
        if User.query.filter_by(email=data['email']).first() and data['email'] != user.email:
            return jsonify({'message': 'Email already exists'}), 409
        user.email = data['email']

    # ... (Add validation and update logic for other fields like profile picture, bio, etc.)

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'}), 200


# Get All Campaigns
@api.route('/campaigns', methods=['GET'])
def get_campaigns():
    from app.models import Campaign
    campaigns = Campaign.query.all()
    return jsonify([campaign.to_dict() for campaign in campaigns]), 200


# Create a New Campaign (Sponsor only)
@api.route('/campaigns', methods=['POST'])
@jwt_required()
def create_campaign():
    from app.models import User
    from app.models import Campaign
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role != 'sponsor':
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Input validation (add more checks as needed)
    required_fields = ['name', 'description', 'start_date', 'end_date', 'budget', 'visibility', 'goals']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400

    # Create a new campaign
    campaign = Campaign(
        name=data['name'],
        description=data['description'],
        start_date=data['start_date'],
        end_date=data['end_date'],
        budget=data['budget'],
        visibility=data['visibility'],
        goals=data['goals'],
        sponsor_id=current_user_id
    )
    db.session.add(campaign)
    db.session.commit()

    return jsonify(campaign.to_dict()), 201


# Get Campaign Details
@api.route('/campaigns/<int:id>', methods=['GET'])
def get_campaign(id):
    from app.models import Campaign
    campaign = Campaign.query.get_or_404(id)
    return jsonify(campaign.to_dict()), 200


# Update Campaign (Sponsor only)
@api.route('/campaigns/<int:id>', methods=['PUT'])
@jwt_required()
def update_campaign(id):
    """
    Updates an existing campaign. Only the sponsor of the campaign or an admin can perform this action.

    Args:
        id: The ID of the campaign to update.

    Returns:
        A JSON response indicating success or failure, along with appropriate status codes.
    """
    from app.models import Campaign
    current_user_id = get_jwt_identity()
    campaign = Campaign.query.get_or_404(id)

    # Authorization check: Only the sponsor or admin can update
    if campaign.sponsor_id != current_user_id and not is_admin():
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Input validation (add more checks as needed)
    valid_fields = ['name', 'description', 'start_date', 'end_date', 'budget', 'visibility', 'goals']
    for field in data:
        if field not in valid_fields:
            return jsonify({'message': f'Invalid field: {field}'}), 400

    # Update campaign fields
    for field in valid_fields:
        if field in data:
            setattr(campaign, field, data[field])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while updating the campaign.'}), 500

    return jsonify({'message': 'Campaign updated successfully', 'campaign': campaign.to_dict()}), 200

# Delete Campaign (Sponsor or Admin only)
@api.route('/campaigns/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_campaign(id):
    from app.models import Campaign
    current_user_id = get_jwt_identity()
    campaign = Campaign.query.get_or_404(id)

    if campaign.sponsor_id != current_user_id and current_user_id != 1:  # Allow admins (id=1)
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign deleted successfully'}), 200


# Get All Ad Requests for a Campaign
@api.route('/campaigns/<int:campaign_id>/ad_requests', methods=['GET'])
@jwt_required()
def get_ad_requests_for_campaign(campaign_id):
    from app.models import Campaign, AdRequest
    current_user_id = get_jwt_identity()
    campaign = Campaign.query.get_or_404(campaign_id)

    # Check if user is the sponsor or an admin
    if current_user_id != campaign.sponsor_id and current_user_id != 1:
        return jsonify({'message': 'Unauthorized'}), 403

    ad_requests = AdRequest.query.filter_by(campaign_id=campaign_id).all()
    return jsonify([ad_request.to_dict() for ad_request in ad_requests]), 200

# Create a New Ad Request (Sponsor only)
@api.route('/campaigns/<int:campaign_id>/ad_requests', methods=['POST'])
@jwt_required()
def create_ad_request(campaign_id):
    from app.models import User
    from app.models import AdRequest
    from app.models import Campaign
    current_user_id = get_jwt_identity()
    campaign = Campaign.query.get_or_404(campaign_id)

    if campaign.sponsor_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Input validation (add more checks as needed)
    required_fields = ['influencer_id', 'message', 'requirements', 'payment_amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing field: {field}'}), 400

    # Check if influencer exists and is active
    influencer = User.query.get(data['influencer_id'])
    if not influencer or not influencer.is_active or influencer.role != 'influencer':
        return jsonify({'message': 'Invalid influencer'}), 400

    # Create a new ad request
    ad_request = AdRequest(
        campaign_id=campaign_id,
        influencer_id=data['influencer_id'],
        message=data['message'],
        requirements=data['requirements'],
        payment_amount=data['payment_amount'],
    )
    db.session.add(ad_request)
    db.session.commit()

    return jsonify(ad_request.to_dict()), 201

# Get Ad Request Details
@api.route('/ad_requests/<int:id>', methods=['GET'])
@jwt_required()
def get_ad_request(id):
    from app.models import AdRequest
    current_user_id = get_jwt_identity()
    ad_request = AdRequest.query.get_or_404(id)

    # Check if user is associated with the ad request (sponsor or influencer)
    if current_user_id != ad_request.campaign.sponsor_id and current_user_id != ad_request.influencer_id:
        return jsonify({'message': 'Unauthorized'}), 403

    return jsonify(ad_request.to_dict()), 200

# Update Ad Request (Sponsor or Influencer)
@api.route('/ad_requests/<int:id>', methods=['PUT'])
@jwt_required()
def update_ad_request(id):
    from app.models import AdRequest
    current_user_id = get_jwt_identity()
    ad_request = AdRequest.query.get_or_404(id)

    # Check if user is associated with the ad request (sponsor or influencer)
    if current_user_id != ad_request.campaign.sponsor_id and current_user_id != ad_request.influencer_id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'message': 'No input data provided'}), 400

    # Update ad request fields (add more fields and validation as needed)
    if 'message' in data:
        ad_request.message = data['message']
    if 'requirements' in data:
        ad_request.requirements = data['requirements']
    if 'payment_amount' in data:
        ad_request.payment_amount = data['payment_amount']
    if 'status' in data:
        ad_request.status = data['status']

    db.session.commit()
    return jsonify({'message': 'Ad Request updated successfully'}), 200

# Delete Ad Request (Sponsor or Admin only)
@api.route('/ad_requests/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ad_request(id):
    from app.models import AdRequest
    current_user_id = get_jwt_identity()
    ad_request = AdRequest.query.get_or_404(id)

    # Check if user is the sponsor or an admin
    if current_user_id != ad_request.campaign.sponsor_id and current_user_id != 1:  # Allow admins (id=1)
        return jsonify({'message': 'Unauthorized'}), 403

    db.session.delete(ad_request)
    db.session.commit()
    return jsonify({'message': 'Ad Request deleted successfully'}), 200




# Get Reports for a Sponsor
@api.route('/reports', methods=['GET'])
@jwt_required()
def get_sponsor_reports():
    from app.models import User, Report
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user.role != 'sponsor':
        return jsonify({'message': 'Unauthorized'}), 403

    reports = Report.query.filter_by(sponsor_id=current_user_id).all()
    return jsonify([report.to_dict() for report in reports]), 200





# Download a Report (Sponsor only)
@api.route('/reports/<int:report_id>', methods=['GET'])
@jwt_required()
def download_report(report_id):
    from app.models import Report
    current_user_id = get_jwt_identity()
    report = Report.query.get_or_404(report_id)

    if report.sponsor_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    # Get the desired format from query parameters (default to PDF)
    output_format = request.args.get('format', 'pdf').lower()

    # Construct the report filename based on the format
    report_filename = f"report_{report.id}.{output_format}"

    # Replace with the actual path to your reports directory
    reports_dir = os.path.join(current_app.root_path, 'reports') 
    report_path = os.path.join(reports_dir, report_filename)

    try:
        if not os.path.isfile(report_path):
            return jsonify({'message': 'Report file not found'}), 404

        # Set the Content-Type header based on the format
        mimetype = 'application/pdf' if output_format == 'pdf' else 'text/csv'

        return send_file(report_path, as_attachment=True, mimetype=mimetype)

    except Exception as e:
        # Log the error for debugging
        print(f"Error downloading report: {e}")
        return jsonify({'message': 'An error occurred while downloading the report'}), 500


@api.route('/categories', methods=['GET'])
def get_categories():
    from app.models import Category
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories]), 200


# Search for Campaigns
@api.route('/search/campaigns', methods=['GET'])
def search_campaigns():
    from app.models import Campaign
    query = request.args.get('q')  # Get the search query from the query parameters
    if not query:
        return jsonify({'message': 'Search query (q) is required'}), 400

    # Basic search implementation (you can customize this based on your needs)
    campaigns = Campaign.query.filter(Campaign.name.ilike(f'%{query}%') | Campaign.description.ilike(f'%{query}%')).all()
    return jsonify([campaign.to_dict() for campaign in campaigns]), 200




@api.route('/search/influencers', methods=['GET'])
def search_influencers():
    from app.models import User
    query = request.args.get('q')
    if not query:
        return jsonify({'message': 'Search query (q) is required'}), 400

    influencers = User.query.filter(
        User.role == 'influencer', 
        User.username.ilike(f'%{query}%') 
    ).all()
    return jsonify([influencer.to_dict() for influencer in influencers]), 200
from flask_jwt_extended import get_jwt_identity
from flask import abort, current_app

import re
from datetime import datetime
import random
import string
from app.models import User

def get_current_user():
    """
    Retrieves the currently authenticated user based on the JWT token.

    Returns:
        User object if authenticated, None otherwise.
    """
    user_id = get_jwt_identity()
    if user_id:
        return User.query.get(user_id)
    return None

def get_current_user_or_401():
    """
    Retrieves the currently authenticated user or raises a 401 error if not authenticated.

    Returns:
        User object if authenticated.

    Raises:
        401 Unauthorized error if not authenticated.
    """
    user = get_current_user()
    if not user:
        abort(401) 
    return user

def is_admin():
    """
    Checks if the current user is an admin.

    Returns:
        True if admin, False otherwise.
    """
    user = get_current_user()
    return user and user.role == 'admin'

# ... (is_sponsor and is_influencer functions remain the same)

def validate_email(email):
    """
    Validates an email address format using a regular expression.

    Args:
        email: The email address to validate.

    Returns:
        True if the email is valid, False otherwise.
    """
    # You can customize the regex pattern for more strict validation if needed
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def send_email(subject, recipients, body, html=None):
    """
    Sends an email using Flask-Mail.

    Args:
        subject: The subject of the email.
        recipients: A list of recipient email addresses.
        body: The plain text body of the email.
        html: (Optional) The HTML body of the email.
    """
    from flask_mail import Message
    from app import mail
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=recipients)
    msg.body = body
    if html:
        msg.html = html
    mail.send(msg)

def format_date(date, format='%Y-%m-%d'):
    """
    Formats a date object into a string using the specified format.

    Args:
        date: The date object to format.
        format: The desired date format string (default is '%Y-%m-%d').

    Returns:
        A formatted date string.
    """
    return date.strftime(format)

def generate_random_password(length=12):
    """
    Generates a random password containing uppercase letters, lowercase letters, digits, and punctuation.

    Args:
        length: The desired length of the password (default is 12).

    Returns:
        A randomly generated password string.
    """

    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in  
 range(length))
    return password

def calculate_influencer_reach(influencer):
    """
    Calculates an influencer's reach based on their followers and engagement metrics.

    Args:
        influencer: The User object representing the influencer.

    Returns:
        The calculated reach value (you'll need to define the specific logic).
    """

    # Placeholder implementation (replace with your actual reach calculation logic)
    # You might need to access additional data from the influencer's profile or social media accounts
    reach = influencer.followers * 0.1  # Example: 10% of followers as reach
    return reach

def calculate_campaign_metrics(campaign):
    """
    Calculates various metrics for a campaign based on its ad requests.

    Args:
        campaign: The Campaign object.

    Returns:
        A dictionary containing calculated metrics (e.g., impressions, clicks, conversions).
    """

    metrics = {
        'impressions': 0,
        'clicks': 0,
        'conversions': 0
        # ... other metrics
    }

    for ad_request in campaign.ad_requests:
        if ad_request.status == 'accepted':
            # Access ad_request data or related models to calculate metrics
            # For example, if you have 'impressions' field in AdRequest:
            metrics['impressions'] += ad_request.impressions  

    return metrics
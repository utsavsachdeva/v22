from celery import shared_task
from app.models import User, AdRequest, Report
from app import db, create_app, mail
from datetime import datetime, timedelta, timezone
import os
from flask_mail import Message
from flask import current_app, render_template


# Placeholder import (replace with actual implementation)
from .report_generator import generate_report, generate_csv_report  

@shared_task
def send_daily_reminders():
    with create_app().app_context():
        # Get influencers who haven't visited or have pending requests in the last 24 hours
        yesterday = datetime.now(timezone.utc) - timedelta(days=1)
        influencers_to_remind = User.query.filter(
            User.role == 'influencer',
            (User.last_login < yesterday) | 
            db.exists().where(AdRequest.influencer_id == User.id, AdRequest.status == 'pending')
        ).all()

        for influencer in influencers_to_remind:
            # Send reminder via email
            send_reminder_email(influencer)

def send_reminder_email(influencer):
    msg = Message("Reminder from Influencer Platform", 
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[influencer.email])
    msg.body = "This is a friendly reminder to check out new ad requests or pending requests on the platform!"
    mail.send(msg)

@shared_task
def generate_monthly_reports():
    with create_app().app_context():
        # Get all sponsors
        sponsors = User.query.filter_by(role='sponsor').all()

        for sponsor in sponsors:
            # Generate report for the past month
            start_date = (datetime.utcnow() - timedelta(days=30)).replace(day=1) 
            end_date = datetime.utcnow().replace(day=1) - timedelta(days=1)

            # Generate the report (assuming PDF format for now)
            
            report_filepath = generate_report(sponsor.id, start_date, end_date, output_format='pdf')

            # Create a Report record in the database
            report = Report(
                sponsor_id=sponsor.id,
                start_date=start_date,
                end_date=end_date,
                report_data={}  # You might want to store some metadata here if needed
            )
            db.session.add(report)
            db.session.commit()

            # Send the report via email
            send_report_email(sponsor, report_filepath,report)

def send_report_email(sponsor, report_filepath, report):
    """
    Sends a monthly activity report email to a sponsor.

    Args:
        sponsor: The User object representing the sponsor.
        report_filepath: The file path to the generated report.
        report: The Report object containing report metadata.
    """

    try:
        subject = "Monthly Activity Report"
        recipients = [sponsor.email]

        # Render the email template with the sponsor's information and report details
        html_content = render_template(
            'report_email.html', 
            sponsor=sponsor, 
            start_date=report.start_date, 
            end_date=report.end_date
        )

        # Create the email message
        msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=recipients, html=html_content)

        # Attach the report file
        with open(report_filepath, 'rb') as f:
            # Determine the MIME type based on the file extension
            file_ext = os.path.splitext(report_filepath)[1].lower()
            mimetype = 'application/pdf' if file_ext == '.pdf' else 'text/csv' 
            msg.attach(f"report_{report.id}{file_ext}", mimetype, f.read())

        # Send the email
        mail.send(msg)

    except Exception as e:
        # Log the error for debugging
        print(f"Error sending report email to {sponsor.email}: {e}")
        # You might want to handle the error differently (e.g., retry sending, notify admin)
        # For now, we'll just re-raise the exception so it can be handled by Celery
        raise

@shared_task
def export_campaign_data_to_csv(sponsor_id):
    with create_app().app_context():
        # Generate CSV report for the sponsor's campaigns
        csv_data = generate_csv_report(sponsor_id)

        # Save the CSV file 
        filename = f"campaign_report_{sponsor_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join('reports', filename)  # Adjust the path
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            f.write(csv_data)

        # Send a notification email to the sponsor
        send_csv_export_notification(sponsor_id)

def send_csv_export_notification(sponsor_id):
    """
    Sends a notification email to a sponsor when their CSV export is complete.

    Args:
        sponsor_id: The ID of the sponsor.
    """

    try:
        sponsor = User.query.get(sponsor_id)
        
        if not sponsor:
            raise ValueError(f"Sponsor with ID {sponsor_id} not found.")

        subject = "CSV Export Complete"
        recipients = [sponsor.email]

        # Render the email template with the sponsor's information
        html_content = render_template('csv_export_notification.html', sponsor=sponsor)

        # Create the email message
        msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=recipients, html=html_content)

        # Send the email
        mail.send(msg)

    except Exception as e:
        # Log the error for debugging
        print(f"Error sending CSV export notification to sponsor {sponsor_id}: {e}")
        # You might want to handle the error differently (e.g., retry sending, notify admin)
        raise  
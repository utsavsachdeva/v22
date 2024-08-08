import csv
from io import StringIO
from app.models import Campaign, AdRequest
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
def generate_report(sponsor_id, start_date, end_date, output_format='pdf'):
    """
    Generates a report (PDF or HTML) for a sponsor's campaigns within a specified date range.

    Args:
        sponsor_id: The ID of the sponsor.
        start_date: The start date of the report period.
        end_date: The end date of the report period.
        output_format: The desired output format ('pdf' or 'html'). Defaults to 'pdf'.

    Returns:
        The path to the generated report file.
    """

    try:
        # 1. Query the database to get campaign data 
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).filter(
            Campaign.start_date >= start_date,
            Campaign.end_date <= end_date
        ).all()

        # 2. Process the data and calculate relevant metrics
        report_data = []
        for campaign in campaigns:
            ad_requests = AdRequest.query.filter_by(campaign_id=campaign.id).all()
            total_ad_requests = len(ad_requests)
            accepted_ad_requests = len([req for req in ad_requests if req.status == 'accepted'])
            pending_ad_requests = len([req for req in ad_requests if req.status == 'pending'])

            # Additional Metrics 
            total_reach = sum([req.influencer.reach for req in ad_requests if req.status == 'accepted'])  
            total_spend = sum([req.payment_amount for req in ad_requests if req.status == 'accepted'])
            avg_payment_per_influencer = total_spend / accepted_ad_requests if accepted_ad_requests > 0 else 0

            report_data.append({
                'campaign_id': campaign.id,
                'campaign_name': campaign.name,
                'start_date': campaign.start_date.strftime('%Y-%m-%d'),
                'end_date': campaign.end_date.strftime('%Y-%m-%d'),
                'budget': campaign.budget,
                'total_ad_requests': total_ad_requests,
                'accepted_ad_requests': accepted_ad_requests,
                'pending_ad_requests': pending_ad_requests,
                'total_reach': total_reach,
                'total_spend': total_spend,
                'avg_payment_per_influencer': avg_payment_per_influencer
            })

        # Handle empty report_data
        if not report_data:
            report_data = [{ 
                'campaign_id': None,
                'campaign_name': 'No campaigns found for this period',
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'budget': 0,
                'total_ad_requests': 0,
                'accepted_ad_requests': 0,
                'pending_ad_requests': 0,
                'total_reach': 0,
                'total_spend': 0,
                'avg_payment_per_influencer': 0
            }]

        # Prepare data for charts
        chart_labels = [campaign['campaign_name'] for campaign in report_data]
        budget_data = [campaign['budget'] for campaign in report_data]
        total_spend_data = [campaign['total_spend'] for campaign in report_data]
        total_ad_requests_data = [campaign['total_ad_requests'] for campaign in report_data]
        accepted_ad_requests_data = [campaign['accepted_ad_requests'] for campaign in report_data]
        pending_ad_requests_data = [campaign['pending_ad_requests'] for campaign in report_data]

        # 3. Generate the report (PDF or HTML)
        env = Environment(loader=FileSystemLoader('app/templates'))
        template = env.get_template('report_template.html')
        html_content = template.render(
            report_data=report_data, 
            start_date=start_date, 
            end_date=end_date,
            chart_labels=chart_labels,
            budget_data=budget_data,
            total_spend_data=total_spend_data,
            total_ad_requests_data=total_ad_requests_data,
            accepted_ad_requests_data=accepted_ad_requests_data,
            pending_ad_requests_data=pending_ad_requests_data
        )

        if output_format == 'pdf':
            filename = f'report_{sponsor_id}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.pdf'
            filepath = os.path.join('reports', filename) 
            HTML(string=html_content).write_pdf(filepath)
        else: 
            filename = f'report_{sponsor_id}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.html'
            filepath = os.path.join('reports', filename)
            with open(filepath, 'w') as f:
                f.write(html_content)

        return filepath

    except Exception as e:
        print(f"Error generating report: {e}")
        raise 


# ... (generate_csv_report function remains the same)

def generate_csv_report(sponsor_id):
    """
    Generates a CSV report for a sponsor's campaigns.

    Args:
        sponsor_id: The ID of the sponsor.

    Returns:
        A CSV string containing campaign data.
    """

    try:
        # 1. Query the database to get campaign data for the sponsor
        campaigns = Campaign.query.filter_by(sponsor_id=sponsor_id).all()

        # 2. Format the data into a CSV string
        output = StringIO()
        writer = csv.writer(output)

        # Write the header row
        header = ['Campaign ID', 'Campaign Name', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals']
        writer.writerow(header)

        for campaign in campaigns:
            row = [
                campaign.id,
                campaign.name,
                campaign.start_date.strftime('%Y-%m-%d'),
                campaign.end_date.strftime('%Y-%m-%d'),
                campaign.budget,
                campaign.visibility,
                campaign.goals
            ]
            writer.writerow(row)

        # Get the CSV data as a string
        csv_data = output.getvalue()

        # 3. Return the CSV string
        return csv_data

    except Exception as e:
        # Log the error
        print(f"Error generating CSV report: {e}")
        raise 

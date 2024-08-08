from app import create_app  # Import your Flask app factory function

app = create_app()  # Create the Flask app instance

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode for development

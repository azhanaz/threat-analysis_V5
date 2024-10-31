from flask import Flask

app = Flask(__name__)

# Add any app-specific configurations here
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG'] = True

from app import routes  # Import routes after the app has been initialized

from flask import Flask 
from flask_cors import CORS
from flaskext.mysql import MySQL
from dotenv import load_dotenv, find_dotenv
import os
from .config import config

mysql = MySQL()

def create_app():
    # Find and load the .env file
    load_dotenv(override=True)

    # Create Flask app
    app = Flask(__name__)
    CORS(app)

    # Choose configuration mode
    env = os.getenv('FLASK_ENV', 'development')
    print(f"Running in {env} mode")
    
    # Load config
    app.config.from_object(config[env])

    # Set MySQL configuration using DATABASE prefix
    app.config.update(
        MYSQL_DATABASE_HOST=os.getenv('MYSQL_HOST'),
        MYSQL_DATABASE_USER=os.getenv('MYSQL_USER'),
        MYSQL_DATABASE_PASSWORD=os.getenv('MYSQL_PASSWORD'),
        MYSQL_DATABASE_DB=os.getenv('MYSQL_DB'),
        MYSQL_DATABASE_PORT=int(os.getenv('MYSQL_PORT'))
    )

    # Initialize MySQL with debug info
    try:
        mysql.init_app(app)
    except Exception as e:
        print(f"Error initializing MySQL: {str(e)}")

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app
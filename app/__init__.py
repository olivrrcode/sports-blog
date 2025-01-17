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
            
    print("\nEnvironment Variables:")
    print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
    print(f"MYSQL_USER: {os.getenv('MYSQL_USER')}")
    print(f"MYSQL_DB: {os.getenv('MYSQL_DB')}")
    print(f"MYSQL_PORT: {os.getenv('MYSQL_PORT')}")

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
        print("MySQL Configuration:")
        print(f"Host: {app.config['MYSQL_DATABASE_HOST']}")
        print(f"User: {app.config['MYSQL_DATABASE_USER']}")
        print(f"Database: {app.config['MYSQL_DATABASE_DB']}")
        print(f"Port: {app.config['MYSQL_DATABASE_PORT']}")
    except Exception as e:
        print(f"Error initializing MySQL: {str(e)}")

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app
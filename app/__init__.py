from flask import Flask 
from flask_cors import CORS
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from .config import config

mysql = MySQL()

def create_app():
    load_dotenv(override=True)
    app = Flask(__name__)
    CORS(app)

    env = os.getenv('FLASK_ENV', 'development')
    print(f"Running in {env} mode")
    
    app.config.from_object(config[env])

    # Update MySQL configuration
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
    app.config['MYSQL_SSL_MODE'] = 'DISABLED'  # Add this line to disable SSL
    
    try:
        mysql.init_app(app)
        print("MySQL initialized successfully")
    except Exception as e:
        print(f"Error initializing MySQL: {str(e)}")

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)

    return app
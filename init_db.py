from sports_blog import create_app
from sports_blog.db import init_db

# Create the application instance
app = create_app()

# Run database initialization within app context
with app.app_context():
    init_db()
    print("Initialized the database.")
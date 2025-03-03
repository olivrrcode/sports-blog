from sports_blog import create_app

# Create the application instance
app = create_app()

if __name__ == '__main__':
    # Run the app with the development server
    app.run(debug=True)
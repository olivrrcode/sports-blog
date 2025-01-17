from flask import Blueprint, jsonify
from app import mysql

main = Blueprint('main', __name__)

@main.route('/')
def index():
    conn = None
    cursor = None
    try:
        # Get a database connection and create a cursor
        conn = mysql.get_db()
        cursor = conn.cursor()

        # Example query
        cursor.execute("SELECT * from dummyData")
        result = cursor.fetchall()

        # If there are results, process them into a list of dictionaries
        if result:
            # Get column names for the response
            columns = [desc[0] for desc in cursor.description]
            data = [dict(zip(columns, row)) for row in result]

            return jsonify({'data': data})

        return jsonify({'message': 'No data found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Ensure resources are always cleaned up
        if cursor:
            cursor.close()
        if conn:
            conn.close()

import hashlib
import json
import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# --- Database Functions ---

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT", 5432) # Default PostgreSQL port
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error: Could not connect to the database. {e}")
        return None

def is_hash_in_db(data_hash):
    """Checks if a hash already exists in the database."""
    conn = get_db_connection()
    if conn is None:
        return True # Assume redundancy if DB connection fails to prevent bad data
        
    exists = False
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM unique_data WHERE data_hash = %s;", (data_hash,))
            exists = cur.fetchone() is not None
    finally:
        conn.close()
    return exists

def add_data_to_db(data_hash, data_dict):
    """Adds a new data entry to the database."""
    conn = get_db_connection()
    if conn is None:
        return False

    success = False
    try:
        with conn.cursor() as cur:
            # Use json.dumps to convert the dictionary to a JSON string
            cur.execute(
                "INSERT INTO unique_data (data_hash, data_content) VALUES (%s, %s);",
                (data_hash, json.dumps(data_dict))
            )
        conn.commit()
        print("Successfully added new unique data to the database.")
        success = True
    except Exception as e:
        print(f"Error adding data to DB: {e}")
        conn.rollback() # Rollback changes on error
    finally:
        conn.close()
    return success

# --- Core Logic Functions ---

def generate_hash(data_dict):
    """Generates a SHA-256 hash for a dictionary to ensure uniqueness."""
    # Convert dictionary to a consistent, sorted string format to ensure the hash is always the same
    data_string = json.dumps(data_dict, sort_keys=True).encode('utf-8')
    return hashlib.sha256(data_string).hexdigest()

def is_data_valid(data_dict):
    """
    Validates that the incoming data has the required fields.
    For this example, we'll check for 'name' and 'email'.
    """
    if not isinstance(data_dict, dict):
        return False
        
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data_dict or not data_dict[field]:
            return False
    return True

# --- API Endpoint ---

@app.route('/add-data', methods=['POST'])
def add_data_endpoint():
    """API endpoint to receive, validate, and store new data."""
    # 1. Get data from the request
    new_data = request.get_json()
    if not new_data:
        return jsonify({"status": "error", "message": "Invalid JSON payload."}), 400

    # 2. Validate the data structure and content
    if not is_data_valid(new_data):
        return jsonify({"status": "error", "message": "Invalid or missing data. 'name' and 'email' are required."}), 400

    # 3. Generate a unique hash for the data
    data_hash = generate_hash(new_data)

    # 4. Check for redundancy in the database
    if is_hash_in_db(data_hash):
        return jsonify({
            "status": "redundant",
            "message": "This exact data already exists in the database."
        }), 200 # 200 OK is appropriate as the server understood and processed the request

    # 5. Add to database if it's unique
    if add_data_to_db(data_hash, new_data):
        return jsonify({
            "status": "success",
            "message": "Unique data has been successfully added.",
            "hash": data_hash
        }), 201 # 201 Created is the correct status for a successful new resource creation
    else:
        return jsonify({"status": "error", "message": "Failed to add data to the database."}), 500


# To run the app locally for testing
if __name__ == '__main__':
    app.run(debug=True)
# The app will run on http://127.0.0.1:5000
from flask import Flask, render_template
from database import db_connect
import os

# Initialize the Flask app
app = Flask(__name__)

# Initialize the MySQL database connection using environment variables
db = db_connect(
    host=os.getenv('MYSQL_HOST', 'mariadb'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', ''),
    database=os.getenv('MYSQL_DATABASE', ''),
)

# Create Flask routes
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
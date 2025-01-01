from flask import Flask
from views import api_blueprint

# Create the Flask application instance
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

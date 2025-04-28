from flask import Flask, g, jsonify, render_template, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from routes import Auth, Users
from flask_cors import CORS
from utils.db import get_db
from utils.security import SecurityUserController



app = Flask(__name__)
CORS(app)
swaggerui_blueprint = get_swaggerui_blueprint(
    '/docs',
    '/openapi.json',
    config={ 
        'app_name': "Gamer Vault LTS"
    }
)
app.register_blueprint(Auth.auth_route)
app.register_blueprint(Users.user_route)
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/token')
def token():
    return SecurityUserController.generar_token_authorizer('22480e7a-4755-46b0-9cfb-983d2a56c348')
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/openapi.json')
def openapi(): 
    return send_from_directory('.', 'openapi.json', mimetype='application/json')

@app.before_request
def before_request():
    g.db = next(get_db())

@app.teardown_request
def teardown_request(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
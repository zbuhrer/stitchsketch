# api_gateway.py

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import jwt
import datetime


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SECRET_KEY'] = 'your_secret_key'

class Router:
    def __init__(self):
        self.routes = {}

    def register_route(self, endpoint, handler):
        self.routes[endpoint] = handler

    def get_handler(self, endpoint):
        return self.routes.get(endpoint)

class AuthService:
    def verify_token(self, token):
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            return True
        except:
            return False

    def generate_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

class APIGateway:
    def __init__(self):
        self.router = Router()
        self.auth_service = AuthService()

        # Register routes
        self.router.register_route('/auth', self.auth_handler)
        self.router.register_route('/images', self.image_handler)
        self.router.register_route('/models', self.model_handler)
        self.router.register_route('/upholstery', self.upholstery_handler)
        self.router.register_route('/visualize', self.visualize_handler)
        self.router.register_route('/users', self.user_handler)

    def route_request(self, endpoint, method, data):
        handler = self.router.get_handler(endpoint)
        if handler:
            return handler(method, data)
        else:
            return jsonify({'error': 'Endpoint not found'}), 404

    def authenticate_request(self, token):
        return self.auth_service.verify_token(token)

    def handle_response(self, response):
        return jsonify(response)

    def auth_handler(self, method, data):
        if method == 'POST':
            # Dummy user validation
            if data.get('username') == 'admin' and data.get('password') == 'password':
                token = self.auth_service.generate_token(1)
                return jsonify({'token': token}), 200
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
        else:
            return jsonify({'error': 'Method not allowed'}), 405

    def image_handler(self, method, data):
        # Placeholder for image processing service
        return jsonify({'message': 'Image processed'}), 200

    def model_handler(self, method, data):
        # Placeholder for 3D reconstruction service
        return jsonify({'message': 'Model reconstructed'}), 200

    def upholstery_handler(self, method, data):
        # Placeholder for upholstery service
        return jsonify({'message': 'Upholstery processed'}), 200

    def visualize_handler(self, method, data):
        # Placeholder for visualization service
        return jsonify({'message': 'Visualization processed'}), 200

    def user_handler(self, method, data):
        # Placeholder for user and project management service
        return jsonify({'message': 'User management processed'}), 200

api_gateway = APIGateway()

class GatewayResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or not api_gateway.authenticate_request(token):
            return jsonify({'error': 'Unauthorized'}), 401

        endpoint = request.path
        method = request.method
        data = request.get_json() if request.is_json else request.form

        response, status_code = api_gateway.route_request(endpoint, method, data)
        return api_gateway.handle_response(response), status_code

api.add_resource(GatewayResource, '/auth', '/images', '/models', '/upholstery', '/visualize', '/users')

if __name__ == '__main__':
    app.run(debug=True)
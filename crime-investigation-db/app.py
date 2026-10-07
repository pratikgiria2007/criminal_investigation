from flask import Flask
from flask_cors import CORS
from config import Config

# Import blueprints
from routes.dashboard import dashboard_bp
from routes.cases import cases_bp
from routes.suspects import suspects_bp
from routes.evidence import evidence_bp
from routes.auth import auth_bp
from routes.officers import officers_bp
from routes.witnesses import witnesses_bp
from routes.interrogations import interrogations_bp
from routes.crime_scenes import crime_scenes_bp
from routes.forensics import forensics_bp

def create_app():
    from flask.json.provider import DefaultJSONProvider
    from datetime import date, datetime
    
    class CustomJSONProvider(DefaultJSONProvider):
        def default(self, o):
            if isinstance(o, (date, datetime)):
                return o.isoformat()
            return super().default(o)

    app = Flask(__name__)
    app.json = CustomJSONProvider(app)
    
    app.config.from_object(Config)
    # Ensure SECRET_KEY is set for sessions
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = 'super-secret-key-change-me'
        
    CORS(app)

    # Global before_request to protect routes
    @app.before_request
    def require_login():
        from flask import request, session, redirect
        allowed_routes = ['auth.login', 'auth.register', 'static']
        if request.endpoint and request.endpoint not in allowed_routes:
            if not session.get('user_id'):
                # If API call, return 401, else redirect to login
                if request.path.startswith('/api/'):
                    return {"error": "Unauthorized"}, 401
                return redirect('/login')

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(cases_bp)
    app.register_blueprint(suspects_bp)
    app.register_blueprint(evidence_bp)
    app.register_blueprint(officers_bp)
    app.register_blueprint(witnesses_bp)
    app.register_blueprint(interrogations_bp)
    app.register_blueprint(crime_scenes_bp)
    app.register_blueprint(forensics_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)


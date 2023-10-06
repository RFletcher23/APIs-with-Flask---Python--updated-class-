from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
from blocklist import BLOCKLIST
from flask_sqlalchemy import SQLAlchemy
from db import db
import models
import os
import secrets 
from flask_migrate import Migrate
from dotenv import load_dotenv


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()

#register bluebprints (store.py & item.py files)
#This says if there is an exception that occurs hidden inside an extention of Flask, propagate it into the main app so we can see it.
    app.config["PROPAGATE_EXCEPTIONS"] = True
    # Smorest configuration - title and version that will be in the documentation. Also the open API version. Open API is a standard for API documentation.
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    #Open API URL prefix
    app.config["OPENAPI_URL_PREFIX"] = "/"
    #Documentation config - this tells Flask Smorest to use Swagger for the API documentation and load the code for the documentation from the url below
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    # This connects the flask smorest extension to the flask app
    migrate = Migrate(app, db)
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "198317462132344972830720504793245016556" #secrets.SystemRandom().getrandbits(128) <-- This gives you a long random secret key to use BUT will reset the secret key every time you restart the app, which isn't ideal.
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "That token is revoved. Everyone knows that token is revoked. Why didn't you know that? You should have known that. I am disappointed in you. ", "error": "token_revoked"}), 
            401,
        )
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message": "You need a fresh token to do that you underachieving wretch. ", "error": "token_not_fresh"}),
            401,
        )
    
    @jwt.additional_claims_loader #This allows you to add extra info to a jwt when you create it
    def add_claims_to_jwt(identity): 
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "You're so damn slow the token expired.", "error": "token_expired"}),
            401,
        )
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return(
             jsonify({"message": "You're so damn stupid you can't even use a token right.", "error": "invalid_token"}), 
             401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify({"message": "Your request didn't even have a token you dipshit. Try again.", "error": "invalid_token"}),
            401,
        )
    
    with app.app_context():
        import models

        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
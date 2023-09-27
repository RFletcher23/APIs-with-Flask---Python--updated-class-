from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 #This is a hashing algorithm that is used to hash passwords
from db import db
from models import UserModel
from schemas import UserSchema
from blocklist import BLOCKLIST
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists. Be more unique next time, nobody likes a copycat.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully. Welcome to the shitshow my dude."}, 201
    
@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        # To login, we must verify the user exists and verify the password matches what the hashed value for that password is
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            # If the user exists and the password is correct, then we create an access token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        
        abort(401, message="Invalid username or password. Come on, it's not that hard. You are an absolute dud aren't you?")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) # fresh must be false here otherwise you can use refresh token to get fresh tokens and you don't want that.
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti) # This adds the jti to the blocklist so that it can't be used again. So this will make one non-fresh token for every refresh token.
        return {"access_token": new_token}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"] # You could use .get("jti") here too instead of ["jti"] here and get the same results too.
        BLOCKLIST.add(jti) # This adds the jti to the blocklist so that it can't be used again after the user logs out.
        return {"message": "You logged out successfully. You're still a loser though."}, 201

    
@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
        
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully. Did you want to do that or did you just fuck up again?"}, 200
        
import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import *
from db import db
from models import StoreModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from schemas import StoreSchema



blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        raise {"message": "Wow, look at you! You actually did something right for a change. So proud."}

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True)) #Multiuple store schemas can be returned so we use many=True here
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists. Your memory is comparable to that of a really dumb goldfish.")
        except SQLAlchemyError:
            abort(500, message="An error occurred when creating the store. Must be your fault, you're the only one dumb enough to make an error like that.")

        return store

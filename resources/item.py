from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import *
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask


blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
    
    
    @jwt_required()
    def delete(self, item_id):
          jwt = get_jwt()
          if not jwt.get("is_admin"):
              abort(401, message="Sorry, losers can't delete items. Only admins can do that.")

          item = ItemModel.query.get_or_404(item_id)
          db.session.delete(item)
          db.session.commit()
          raise {"message": "Wow, look at you! You actually did something right for a change. Or did you cheat? I bet you cheated."}
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id): #item_data must go in front of the other arguments (but still behinf self) whenever you use the blp decorator
        item = ItemModel.query.get(item_id)

        if item: #if the item exists 
            item.price = item_data["price"] #then update it
            item.name = item_data["name"]
        else: #else, create the item
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True)) #Use many=True when returning multiple item schemas
    def get(self):
        return ItemModel.query.all() #This will return a list with items
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data): 
    #item_data contains json which is the validated fields that the schema requested. 
    #The json is passed through the item schema, it checks that the fields are there, that they're valid types, etc. then it gives the method an argment which is that validated dictionary/data.   
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item. Probably due to the fact that you're stupid.")
        
        return item
    

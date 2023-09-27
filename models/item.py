from db import db

#This creates a mapping between a row in a table to a python class and is therefore a python object
class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True) #id column will pre-populate incrementally starting at 1 and going up from there
    name = db.Column(db.String(80), unique=True, nullable=False) #Column name is a string with max 80 characters, string must be unique and nullable=False means you can't make an item with no name
    description = db.Column(db.String(300), unique=False, nullable=True)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False) 
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False) #The foriegn key indicates that stores.id (the id columm in the stores table) maps to store_id
    store = db.relationship("StoreModel", back_populates="items") #This is a store/StoreModel object
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags") 
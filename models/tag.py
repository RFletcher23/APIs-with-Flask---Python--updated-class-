from db import db

class TagModel(db.Model):
    __tablename__ = 'tags'
    # Define table name and make sure it inherits from db.Model
    # Define columns & column types
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=False) #unique=true here means no two tags can have the same name 
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)

    store = db.relationship('StoreModel', back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")

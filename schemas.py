from marshmallow import Schema, fields

#Creating classes to define data types for validation to make sure when things are created/updated/deleted/etc. that data is correct in case there are optional data fields
class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True) #only want to use this for returning data which means dump_only is set to True
    name = fields.Str(required=True) #No dump_only here because name is both unput and output data. If you did dump_only=true then you could not name an item when creating it. So instead we do required=True
    price = fields.Float(required=True) 

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True) #Again here id will only be used when sending data back
    name = fields.Str(required=True) #Again here a store name is needed so required=True

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()
    #Note that neither name or price have required=true because a user can update one or the other or both

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)

class TagAndItemSchema(Schema): #this schema is for when a tag and an item are related
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True) #load_only=True means that the password will not be sent back to the user when they request it. This is for security reasons.
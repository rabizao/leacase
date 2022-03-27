from marshmallow_sqlalchemy import SQLAlchemySchema, SQLAlchemyAutoSchema, auto_field
from app.models import Album, Client, Order
from marshmallow import fields


class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client

    id = auto_field(dump_only=True)


class AlbumSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Album

    id = auto_field(dump_only=True)


class AlbumQuerySchema(SQLAlchemySchema):

    name = fields.String()
    artist = fields.String()
    launch_year = fields.Integer()
    style = fields.String()


class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Order

    id = auto_field(dump_only=True)
    client = fields.Nested(ClientSchema, dump_only=True)
    album = fields.Nested(AlbumSchema, dump_only=True)


class OrderQuerySchema(SQLAlchemySchema):

    client_id = fields.Integer()
    album_id = fields.Integer()
    timestamp = fields.List(fields.DateTime())


class CreateOrderSchema(SQLAlchemySchema):

    album = fields.Integer(required=True)
    quantity = fields.Integer(dump_default=1)

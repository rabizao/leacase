from app.schemas import ClientSchema, CreateOrderSchema, OrderSchema
from app.models import Album, Client
from . import bp
from flask.views import MethodView
from app import db
from flask_smorest import abort


@bp.route('/clients')
class Clients(MethodView):
    @bp.arguments(ClientSchema)
    @bp.response(201, ClientSchema)
    def post(self, args):
        """Create new client"""
        client = Client(**args)
        db.session.add(client)
        db.session.commit()
        return client


@bp.route('/clients/<int:id>')
class ClientsById(MethodView):
    #TODO: @auth_required decorator to authenticate clients
    @bp.arguments(ClientSchema)
    @bp.response(204)
    def put(self, args, id):
        """Edit existing client"""
        client = Client.query.get(id)
        if not client:
            abort(404)

        client.update(args)
        db.session.commit()

    #TODO: @auth_required decorator to authenticate clients
    @bp.response(204)
    def delete(self, id):
        """Delete existing client"""
        client = Client.query.get(id)
        if not client:
            abort(404)

        client.active = False
        db.session.commit()


@bp.route('/clients/<int:id>/orders')
class ClientsById(MethodView):
    #TODO: @auth_required decorator to authenticate clients
    @bp.arguments(CreateOrderSchema)
    @bp.response(201, OrderSchema)
    def post(self, args, id):
        """Create a new order to client with id <id>"""
        client = Client.query.get(id)
        if not client:
            abort(404)

        album = Album.query.get(args["album"])
        if not album:
            abort(404)

        order = client.new_order(album=album, quantity=args["quantity"])
        if not order:
            abort(422)

        return order

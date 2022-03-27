from app.schemas import AlbumQuerySchema, AlbumSchema
from app.models import Album
from . import bp
from flask.views import MethodView
from app import db
from flask_smorest import abort


@bp.route('/albums')
class Albums(MethodView):
    # TODO: @auth_required decorator to authenticate clients
    @bp.arguments(AlbumSchema)
    @bp.response(201, AlbumSchema)
    def post(self, args):
        """Create new album"""
        album = Album(**args)
        db.session.add(album)
        db.session.commit()
        return album

    @bp.arguments(AlbumQuerySchema, location="query")
    @bp.response(200, AlbumSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List paginated and filtered albums"""
        data, pagination_parameters.item_count = Album.get(args, pagination_parameters.page,
                                                           pagination_parameters.page_size)
        return data


@bp.route('/albums/<int:id>')
class AlbumsById(MethodView):
    # TODO: @auth_required decorator to authenticate clients
    @bp.arguments(AlbumSchema)
    @bp.response(204)
    def put(self, args, id):
        """Edit existing album"""
        album = Album.query.get(id)
        if not album:
            abort(404)

        album.update(args)
        db.session.commit()

    # TODO: @auth_required decorator to authenticate clients
    @bp.response(204)
    def delete(self, id):
        """Delete existing album"""
        album = Album.query.get(id)
        if not album:
            abort(404)

        db.session.delete(album)
        db.session.commit()

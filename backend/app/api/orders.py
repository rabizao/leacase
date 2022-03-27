from app.schemas import OrderQuerySchema, OrderSchema
from app.models import Order
from . import bp
from flask.views import MethodView


@bp.route('/orders')
class Orders(MethodView):
    #TODO: @auth_required decorator to authenticate clients
    @bp.arguments(OrderQuerySchema, location="query")
    @bp.response(200, OrderSchema(many=True))
    @bp.paginate()
    def get(self, args, pagination_parameters):
        """List paginated and filtered orders"""
        data, pagination_parameters.item_count = Order.get(args, pagination_parameters.page,
                                                           pagination_parameters.page_size)
        return data

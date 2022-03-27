from operator import and_
from typing import Union
from app import db
from datetime import datetime
from sqlalchemy import and_, or_


def process_new_order(client: Union['Client', int], album: Union['Album', int], quantity: int) -> Union['Order', None]:
    if isinstance(album, int):
        album = Album.query.get(album)
    if isinstance(client, int):
        client = Client.query.get(client)
    if not client.active:
        return None

    album.quantity = Album.quantity - quantity
    db.session.commit()

    if album.quantity < 0:
        album.quantity = Album.quantity + quantity
        db.session.commit()
        return None

    order = Order(client=client, album=album, quantity=quantity)
    db.session.add(order)
    db.session.commit()
    return order


class PaginatedSearchMixin(object):
    @classmethod
    def get(cls, data, page, page_size, query=None, filter_by={}, filter=[], order_by=None):
        """
        Return a collection of items already paginated of the selected class
        """
        logic = and_ if 'logic' in data and data['logic'] == 'and' else or_
        query = query or cls.query
        data.pop('logic', None)
        search_conds = []
        for key, values in data.items():
            if isinstance(values, list):
                if len(values) == 2 and (all(isinstance(item, int) or all(isinstance(item, datetime))) for item in values):
                    values.sort()
                    search_conds += [getattr(cls, key).between(*values)]
                else:
                    search_conds += [getattr(cls,
                                             key).like(f"%{item}%") for item in values]
            elif isinstance(values, bool):
                search_conds += [getattr(cls, key).is_(values)]
            else:
                search_conds += [getattr(cls, key).like(f"%{values}%")]

        resources = query.filter_by(**filter_by).filter(
            logic(*search_conds)).filter(*filter).order_by(order_by).paginate(page, page_size, False)

        return resources.items, resources.total


class UpdatableMixin(object):
    def update(self, args):
        for key, value in args.items():
            setattr(self, key, value)
        return self


class Album(UpdatableMixin, PaginatedSearchMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    artist = db.Column(db.String(120), index=True)
    launch_year = db.Column(db.Integer, index=True)
    style = db.Column(db.String(120), index=True)
    quantity = db.Column(db.Integer, default=0)
    orders = db.relationship('Order', backref='album', lazy='dynamic')


class Client(UpdatableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String(120))
    full_name = db.Column(db.String(120))
    date_of_birth = db.Column(db.Date)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    orders = db.relationship('Order', backref='client', lazy='dynamic')
    active = db.Column(db.Boolean, default=True)

    def new_order(self, album: Union['Album', int], quantity: int) -> Union['Order', None]:
        return process_new_order(client=self, album=album, quantity=quantity)


class Order(PaginatedSearchMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    quantity = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

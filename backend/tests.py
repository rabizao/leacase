#!/usr/bin/env python
from datetime import timedelta
import unittest
from app import create_app, db
from app.models import Album, Client, Order, process_new_order
from config import Config
import os

mock_client1 = {
    "full_name": "Client 1",
    "email": "test1@test.com"
}

mock_album1 = {
    "name": "We are Reactive",
    "quantity": 500,
    "launch_year": 1970,
    "style": "rock",
    "artist": "Hohpe"
}


class TestConfig(Config):
    TESTING = True
    # Memory is faster ('sqlite://') but test_stress_many_orders_simultaneously won't work
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testdb.db'


class ApiCase(unittest.TestCase):
    def setUp(self):
        if os.path.exists('app/testdb.db'):
            os.remove('app/testdb.db')
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        if os.path.exists('app/testdb.db'):
            os.remove('app/testdb.db')

    def create_client(self, client=mock_client1):
        c = Client(**client)
        db.session.add(c)
        db.session.commit()
        return c

    def create_album(self, album=mock_album1):
        a = Album(**album)
        db.session.add(a)
        db.session.commit()
        return a

    def create_order(self, client=mock_client1, album=mock_album1, quantity=1):
        c = self.create_client(client=client)
        a = self.create_album(album=album)
        order = c.new_order(album=a, quantity=quantity)
        return order

    def test_new_client(self):
        self.create_client()
        self.assertTrue(len(Client.query.all()) == 1)

    def test_new_album(self):
        self.create_album()
        self.assertTrue(len(Album.query.all()) == 1)

    def test_new_order(self):
        album = Album(**mock_album1)
        client = Client(**mock_client1)
        db.session.add(album)
        db.session.add(client)
        db.session.commit()
        # Try to sell a quantity that is current available
        order = client.new_order(
            album=album, quantity=album.quantity)
        self.assertEqual(len(Order.query.all()), 1)
        quantity_after = album.quantity

        self.assertTrue(isinstance(order, Order))
        self.assertEqual(quantity_after, 0)
        # Try to sell a quantity that is NOT current available
        album.quantity = mock_album1["quantity"]
        quantity_before = album.quantity
        order = client.new_order(album=album, quantity=quantity_before+1)
        self.assertFalse(isinstance(order, Order))

    def test_create_album(self):
        response = self.client.post("/api/albums", json=mock_album1)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(len(Album.query.all()) == 1)

    def test_edit_album(self):
        # Create an album first
        album = self.create_album()
        # Edit order
        name_before = album.name
        response = self.client.put(
            f"/api/albums/{album.id}", json={"name": "Edited Name"})
        self.assertEqual(response.status_code, 204)
        name_after = Album.query.get(album.id).name
        self.assertNotEqual(name_before, name_after)
        # Edit invalid client ...

    def test_delete_album(self):
        # Create an album first
        response = self.client.post("/api/albums", json=mock_album1)
        album = Album.query.get(response.get_json()["id"])
        # Delete album
        response = self.client.delete(f"/api/albums/{album.id}")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Album.query.all()), 0)
        # Delete invalid album ...

    def test_create_client(self):
        response = self.client.post("/api/clients", json=mock_client1)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(len(Client.query.all()) == 1)

    def test_edit_client(self):
        # Create a client first
        client = self.create_client()
        # Edit client
        name_before = client.full_name
        response = self.client.put(
            f"/api/clients/{client.id}", json={"full_name": "Edited Name"})
        self.assertEqual(response.status_code, 204)
        name_after = Client.query.get(client.id).full_name
        self.assertNotEqual(name_before, name_after)
        # Edit invalid client ...

    def test_delete_client(self):
        # Create a client first
        client = self.create_client()
        # Delete client
        response = self.client.delete(f"/api/clients/{client.id}")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Client.query.get(client.id).active)
        # Delete invalid client ...

    def test_create_order(self):
        client = self.create_client()
        album = self.create_album()
        response = self.client.post(
            f"/api/clients/{client.id}/orders", json={"album": album.id, "quantity": album.quantity})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Order.query.all()), 1)

    def test_list_albums(self):
        # Create an album first
        album = self.create_album()
        # List all
        response = self.client.get(f"/api/albums")
        results = response.get_json()
        self.assertEqual(len(results), 1)
        # List by style
        response = self.client.get(f"/api/albums?style={album.style}")
        results = response.get_json()
        self.assertEqual(len(results), 1)
        # List by invalid style
        response = self.client.get("/api/albums?style=notvalid")
        results = response.get_json()
        self.assertEqual(len(results), 0)
        # List by launch_year
        response = self.client.get(
            f"/api/albums?launch_year={album.launch_year}")
        results = response.get_json()
        self.assertEqual(len(results), 1)
        # List by invalid launch_year
        response = self.client.get("/api/albums?launch_year=3000")
        results = response.get_json()
        self.assertEqual(len(results), 0)
        # List by artist
        response = self.client.get(f"/api/albums?artist={album.artist}")
        results = response.get_json()
        self.assertEqual(len(results), 1)
        # List by invalid artist
        response = self.client.get("/api/albums?artist=notvalid")
        results = response.get_json()
        self.assertEqual(len(results), 0)
        # List by name
        response = self.client.get(f"/api/albums?name={album.name}")
        results = response.get_json()
        self.assertEqual(len(results), 1)
        # List by invalid name
        response = self.client.get("/api/albums?name=notvalid")
        results = response.get_json()
        self.assertEqual(len(results), 0)

    def test_list_orders(self):
        # Create an order first
        order = self.create_order(
            client=mock_client1, album=mock_album1, quantity=mock_album1["quantity"])
        # List by client_id
        response = self.client.get(f"/api/orders?client_id={order.client_id}")
        results = response.get_json()
        self.assertEqual(len(results), 1)
        # List by invalid client_id
        response = self.client.get("/api/orders?client_id=999")
        results = response.get_json()
        self.assertEqual(len(results), 0)
        # List by timestamp
        delta = timedelta(hours=1)
        delta2 = timedelta(hours=2)
        response = self.client.get(
            f"/api/orders?timestamp={order.timestamp-delta}&timestamp={order.timestamp+delta}")
        results = response.get_json()
        self.assertEqual(len(results), 1)
        # List by invalid timestamp
        response = self.client.get(
            f"/api/orders?timestamp={order.timestamp+delta}&timestamp={order.timestamp+delta2}")
        results = response.get_json()
        self.assertEqual(len(results), 0)

    def test_stress_many_orders_simultaneously(self):
        # Create client and album first
        client = self.create_client()
        album = self.create_album()
        # Perform stress test
        n_requests = 3000
        from multiprocessing import Pool
        with Pool(10) as pool:
            pool.starmap(process_new_order, [
                (client.id, album.id, 1) for _ in range(n_requests)])
        self.assertLessEqual(len(Order.query.all(
        )), album.quantity)
        print("\nOrders processed: ", len(Order.query.all()))


if __name__ == '__main__':
    unittest.main(verbosity=2)

import os

os.environ["DATABASE_URL"] = 'postgresql:///cupcakes_test'

from unittest import TestCase

from app import app
from models import db, Cupcake, connect_db

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# connect_db(app)

db.drop_all()
db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}


class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""

        Cupcake.query.delete()

        # "**" means "pass this dictionary as individual named params"
        cupcake = Cupcake(**CUPCAKE_DATA)
        db.session.add(cupcake)
        db.session.commit()

        self.cupcake_id = cupcake.id

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_cupcakes(self):
        """Tests API call returns all cupcake instances as JSON"""

        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json.copy()

            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake_id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        """Tests API call returns details of one cupcake as JSON"""

        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake_id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        """Tests API call adds new cupcake to database and returns as JSON object"""

        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json.copy()

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)


    def test_patch_cupcake(self):
        """Tests API call updates cupcake details in database and returns as 
        JSON object"""
        
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.patch(
                url,
                json={"flavor": "Updated_Flavor",
                      "size": "Updated_Size",
                      "rating": 10,
                      "image": "http://test.com/cupcake.jpg"
                      }
            )
        
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
              "cupcake": {
              "id": self.cupcake_id,
              "flavor": "Updated_Flavor",
              "size": "Updated_Size",
              "rating": 10,
              "image": "http://test.com/cupcake.jpg"
               }
            })


    def test_delete_cupcake(self):
        """Tests API call deletes cupcake from database and returns JSON deleted 
        notification"""
        
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake_id}"
            resp = client.delete(url)
            
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {"deleted": self.cupcake_id})

            self.assertEqual(Cupcake.query.count(), 0)






import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import os
from flaskr import create_app
from models import setup_db, Supplier, Captain


class AyaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    Bearer = 'Bearer '
    Suppliers_url = '/suppliers'
    Captain_url = '/captains'
    Val_Changed_Bateau = 'changed bateau'
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # in case of varaibale didn t exist(such in our case ,
        # we return spesified values)
        self.database_host = os.getenv('DB_HOST', 'localhost:5432')
        self.database_name = os.getenv('DB_NAME', 'aya_test')
        self.database_path = "postgres://{}/{}".format(self.database_host,
                                                       self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    One test for each test for
    successful operation and for expected errors.
    """
    def test_get_suppliers(self):
        global Bearer
        jwt_token_agent = os.environ.get('AGENT')
        res = self.client().get(self.Suppliers_url,
                                headers={"Authorization": self.Bearer +
                                         jwt_token_agent})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["currentPageContent"])
        self.assertTrue(data["total"])

    def test_400_post_suppliers(self):
        jwt_token_master = os.environ.get('MASTER')
        res = self.client().post(self.Suppliers_url, json={"nameh": "Supp 3"},
                                 headers={"Authorization": self.Bearer +
                                 jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    def test_200_get_suppliers(self):
        jwt_token_master = os.environ.get('MASTER')
        res = self.client().get("/suppliers?page=1",
                                headers={"Authorization": self.Bearer +
                                         jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["currentPageContent"])
        self.assertTrue(data["total"])
        self.assertTrue(data["nbrPages"])

    def test_404_get_suppliers(self):
        jwt_token_agent = os.environ.get('AGENT')
        res = self.client().get("/suppliers?page=10000",
                                headers={"Authorization": self.Bearer +
                                         jwt_token_agent})
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], 'Unprocessable error')

    def test_200_create_new_supplier(self):
        jwt_token_master = os.environ.get('MASTER')
        res = self.client().post("/suppliers", json={"name": "Supp 7 test"},
                                 headers={"Authorization": self.Bearer +
                                 jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["nbrPages"])

    def test_200_patch_existing_supplier(self):
        jwt_token_master = os.environ.get('MASTER')
        currentsupplier = Supplier.query.all()[0]
        currentsupplier.name = "changed supplier"
        res = self.client().patch("/suppliers", json=currentsupplier.format(),
                                  headers={"Authorization": self.Bearer +
                                           jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["supplier"]["name"], self.Val_Changed_Bateau)

    def test_200_delete_suppliers(self):
        jwt_token_master = os.environ.get('MASTER')
        # select existing question
        current_supp = Supplier.query.order_by(Supplier.id).all()[0]

        res = self.client().delete("/suppliers/"+str(current_supp.id),
                                   headers={"Authorization": self.Bearer +
                                   jwt_token_master})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], current_supp.id)
        self.assertTrue(data["contentCurrentPage"])
        self.assertTrue(data["total"])

    def test_422_delete_non_existing_supplier(self):
        jwt_token_master = os.environ.get('MASTER')
        res = self.client().delete("/suppliers/100000",
                                   headers={"Authorization": self.Bearer +
                                            jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], 'resource not found')

    '''
     Endpoints for Captain
    '''
    def test_get_captains(self):
        jwt_token_master = os.environ.get('MASTER')
        res = self.client().get(self.Captain_url,
                                headers={"Authorization": self.Bearer +
                                         jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["currentPageContent"])
        self.assertTrue(data["total"])

    def test_400_post_captains(self):
        jwt_token_master = os.environ.get('MASTER')
        res = self.client().post(self.Captain_url,
                                 json={"nameeee": "Mohamed Ali",
                                       "bateau": "Bateau Elvela7"},
                                 headers={"Authorization": self.Bearer +
                                          jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    def test_200_get_captains(self):
        jwt_token_agent = os.environ.get('AGENT')
        res = self.client().get("/captains?page=1",
                                headers={"Authorization": self.Bearer +
                                         jwt_token_agent})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["currentPageContent"])
        self.assertTrue(data["total"])
        self.assertTrue(data["nbrPages"])

    def test_404_get_captains(self):
        jwt_token_agent = os.environ.get('AGENT')
        res = self.client().get("/captains?page=10000",
                                headers={"Authorization": self.Bearer +
                                         jwt_token_agent})
        data = json.loads(res.data)
        print(data)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 422)
        self.assertEqual(data["message"], 'Unprocessable error')

    def test_200_create_new_captains(self):
        jwt_token_master = os.environ.get('MASTER')
        res = self.client().post(self.Captain_url,
                                 json={"name": "Mohamed Ali",
                                       "bateau": "Bateau Elvela7"},
                                 headers={"Authorization": self.Bearer +
                                          jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["nbrPages"])

    def test_200_patch_existing_captains(self):
        jwt_token_master = os.environ.get('MASTER')
        currentcaptain = Captain.query.all()[0]
        currentcaptain.bateau = self.Val_Changed_Bateau
        res = self.client().patch(self.Captain_url,
                                  json=currentcaptain.format(),
                                  headers={"Authorization": self.Bearer +
                                           jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["captain"]["bateau"], self.Val_Changed_Bateau)

    def test_200_delete_captains(self):
        jwt_token_master = os.environ.get('MASTER')
        current_captain = Captain.query.order_by(Captain.id).all()[0]
        res = self.client().delete("/captains/"+str(current_captain.id),
                                   headers={"Authorization": self.Bearer +
                                   jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], current_captain.id)
        self.assertTrue(data["contentCurrentPage"])
        self.assertTrue(data["total"])

    def test_422_delete_non_existing_captains(self):
        jwt_token_master = os.environ.get('MASTER')
        res = self.client().delete("/captains/100000",
                                   headers={"Authorization": self.Bearer +
                                            jwt_token_master})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertEqual(data["message"], 'resource not found')


if __name__ == "__main__":
    unittest.main()

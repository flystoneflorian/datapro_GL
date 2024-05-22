import unittest
from app_functions import check_credentials, load_data, create_melted_db
import pandas as pd

class TestAppFunctions(unittest.TestCase):

    def setUp(self):
        self.db_path = 'my_database.db'

    def test_check_credentials(self):
        self.assertTrue(check_credentials("admin", "1234"))
        self.assertFalse(check_credentials("wrong_user", "1234"))
        self.assertFalse(check_credentials("admin", "wrong_pass"))

    def test_load_data(self):
        # Utiliser load_data pour lire les données
        loaded_data = load_data(self.db_path)
        
        # Vérifier que les données sont correctement chargées
        self.assertGreater(loaded_data.shape[0], 0)  # Vérifie qu'il y a des lignes dans le DataFrame
        self.assertEqual(loaded_data['DATE'].dtype, 'datetime64[ns]')

    def test_create_melted_db(self):
        complete = load_data(self.db_path) 
        # Utiliser create_melted_db pour transformer les données
        melted_db = create_melted_db(complete)       
        # Vérifier que les données sont correctement transformées
        self.assertGreater(melted_db.shape[0], 0)  # Vérifie qu'il y a des lignes dans le DataFrame transformé

if __name__ == '__main__':
    unittest.main()


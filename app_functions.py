import pandas as pd
import sqlite3

DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "1234"

def check_credentials(username, password):
    return username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD

def load_data(db_path='my_database.db'):
    conn = sqlite3.connect(db_path)
    complete = pd.read_sql('SELECT * FROM complete', conn)
    conn.close()
    complete['DATE'] = pd.to_datetime(complete['DATE'])
    return complete

def create_melted_db(complete):
    return pd.melt(complete, id_vars=['DATE', 'COLLECTE', 'ID', 'CSP', 'ENFANTS', 'PRIX'], var_name='SECTEUR', value_name='DEPENSE')

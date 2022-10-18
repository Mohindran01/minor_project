from app import *
import psycopg2
def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='minor',
                            user='postgres',
                            password='password')
    return conn


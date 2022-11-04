from app import *
from constants import *
import psycopg2
def get_db_connection():
    
    conn = psycopg2.connect(host=hosts,
                            database=databases,
                            user=users,
                            password=passwords)
    return conn


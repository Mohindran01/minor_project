from app import *
import psycopg2
def get_db_connection():
    conn = psycopg2.connect(host='ec2-3-213-66-35.compute-1.amazonaws.com',
                            database='dbjb1b02k0uu4c',
                            user='ndoxopmrmkwvtm',
                            password='f08c1327a23c31e9e55f28308b018255832b41f879efbf5a69e139b89786267a')
    return conn


from dotenv import load_dotenv
import os
import psycopg2

#CONEXÃO COM O BANCO
def conectar_banco():
    conn =psycopg2.connect(
        host = 'localhost',
        database = 'Soccer_Stats',
        user = 'postgres',
        password = 'senha123',
        port='5432'
    )
    return conn

def conectar_banco_nuvem():
    load_dotenv(dotenv_path="./.env")
    SERVICE_URI = os.getenv('SERVICE_URI')
    print(SERVICE_URI)
    conn = psycopg2.connect(SERVICE_URI)

    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    print(version)
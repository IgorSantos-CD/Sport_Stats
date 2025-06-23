import pandas as pd
import psycopg2
from psycopg2 import sql

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
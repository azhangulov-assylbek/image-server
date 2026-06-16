# import psycopg
# import os
#
# from psycopg import postgres
#
#
# def get_connection():
#     return psycopg.connect(
#         dbname='images_db',
#         user='postgres',
#         password='password',
#         host='localhost',
#         port='5435'
#     )
# верхняя часть кода давала ошибки в docker. пробую с измененным кодом.
import os

import psycopg


def get_connection():
    return psycopg.connect(
        dbname=os.getenv('DB_NAME', 'images_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', '5432'),
    )
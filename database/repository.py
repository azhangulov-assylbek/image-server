import logging

from database.db import get_connection

def save_metadata(filename:str,original_name:str, size:int,file_type:str)->None:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO images (filename,original_name, size, file_type)
                VALUES (%s,%s,%s,%s)'''
                cursor.execute(sql,(filename,original_name,size,file_type))
                conn.commit()
                logging.info(f'База данных:метаданные для {filename} сохранены')
    except Exception as e:
        conn.rollback()
        logging.error(f'База данных: ошибка сохранения данных {e}')

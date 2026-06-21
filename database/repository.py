import logging

from database.db import get_connection

def save_metadata(filename:str,original_name:str, size:int,file_type:str)->None:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                sql = '''INSERT INTO images (filename,original_name, size, file_type)
                VALUES (%s,%s,%s,%s);'''
                cursor.execute(sql,(filename,original_name,size,file_type))
                conn.commit()
                logging.info(f'База данных:метаданные для {filename} сохранены')
    except Exception as e:
     #  conn.rollback()
        logging.error(f'База данных: ошибка сохранения данных {e}')
        raise

def get_images(per_page: int,offset: int)  :
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:

                cursor.execute('''
                SELECT id,filename,original_name,size,upload_date,file_type 
                FROM images
                ORDER BY upload_date DESC
                LIMIT %s OFFSET %s;    
                ''',(per_page,offset))
                rows = cursor.fetchall()
        return rows

    except Exception as e:
        logging.error(f'Не удалось извлечь данные из базы данных : {e}')
        raise

def get_count_images():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT COUNT(*) FROM images')
                total = cursor.fetchone()[0]
                return total
    except Exception as e:
        logging.error(f'Не удалось извлечь данные из базы данных : {e}')
        raise

# функция удаления загруженного файла
def delete_metadata(image_id: int) -> str | None:
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute('DELETE FROM images WHERE id = %s RETURNING filename;', (image_id,))
                row = cursor.fetchone()
                conn.commit()
                if row is None:
                    logging.warning(f'База данных: запись id={image_id} не найдена')
                    return None
                logging.info(f'База данных: запись id={image_id} ({row[0]}) удалена')
                return row[0]
    except Exception as e:
        logging.error(f'База данных: ошибка удаления данных {e}')
        raise
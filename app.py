from flask import Flask,render_template,jsonify,request,send_from_directory,url_for,redirect,abort
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge
import logging
import uuid
import os
from io import BytesIO
from pathlib import Path

from database.repository import save_metadata, get_images, get_count_images,delete_metadata

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path(os.getenv('IMAGES_DIR',BASE_DIR / 'images'))

LOGS_DIR = Path(os.getenv('LOGS_DIR',BASE_DIR / 'logs'))

MAX_FILE_SIZE = 5*1024*1024

REQUEST_LIMIT = MAX_FILE_SIZE + 1024 * 1024

ALLOWED_IMAGE_FORMATS = {
    'JPEG': ['.jpg', '.jpeg'],
    'PNG': ['.png'],
    'GIF': ['.gif', '.gifv'],
    }

app.config['MAX_CONTENT_LENGTH'] = REQUEST_LIMIT

IMAGES_DIR.mkdir(exist_ok=True)

LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / 'app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

def detect_image_extension(file_data: bytes):
    try:
        with Image.open(BytesIO(file_data)) as image:
            image.verify()
            extensions = ALLOWED_IMAGE_FORMATS.get(image.format)
            return extensions[0] if extensions else None
    except (UnidentifiedImageError, OSError):
        return None
@app.get("/")
def home():
    return render_template("index.html")


@app.get("/upload")
def upload_page():
    return render_template("upload.html")



@app.post('/upload')
def upload_image():
    uploaded_file = request.files.get('image')
    print(uploaded_file)
    if uploaded_file is None:
        logging.warning('Ошибка: файл image не найден в запросе')
        return jsonify({
            'error':'Файл не найден. Поле формы должно называться image'
        })

    original_filename= uploaded_file.filename or 'unknown'

    file_data = uploaded_file.read()

    if not file_data:
        logging.warning(f'Ошибка: файл {original_filename} не должен быть пустым')
        return jsonify({
                'error': 'Пустой файл'
        }),400

    if len(file_data) > MAX_FILE_SIZE:
        logging.warning(f'Ошибка: файл {original_filename} не должен быть больше 5МВ')
        return jsonify({
            'error': 'Файл не может быть больше 5 Мб'
        })

    image_extension = detect_image_extension(file_data)

    if image_extension is None:
        logging.warning(f'Ошибка: неподдерживаемый или поврежденный файл')
        return jsonify({
            'error': 'Поддерживаются только форматы jpg,png,gif'
        })

    unique_filename = f'{uuid.uuid4().hex}{image_extension}'

    target_path= IMAGES_DIR / unique_filename

    target_path.write_bytes(file_data)
    try:
        save_metadata(
            filename=unique_filename,
            original_name=original_filename,
            size=len(file_data),
            file_type=image_extension
        )
    except Exception as e:
        target_path.unlink(missing_ok=True)
        logging.error(f'Файл удален, потому что не удалось сохранить метаданные')
        return jsonify({'error':"Ошибка при сохранении данных"}),500

    relative_url= url_for('get_image',filename=unique_filename)
    full_url= request.host_url.rstrip('/') + relative_url
    logging.info(f'Успех. Изображение загружено как {original_filename}')
    return jsonify(
        {
        'message':'Изображение успешно загружено',
        'id': unique_filename,
        'url':full_url,
        }
    ),201


@app.post('/images/<path:filename>/delete')
def delete_image(filename):
    page = request.form.get('page', 1, type=int)

    # Безопасность: путь должен оставаться внутри папки images (защита от ../../)
    images_root = IMAGES_DIR.resolve()
    target_path = (IMAGES_DIR / filename).resolve()
    if not target_path.is_relative_to(images_root):
        logging.warning(f'Удаление отклонено: подозрительный путь {filename}')
        abort(404)

    target_path.unlink(missing_ok=True)   # удаляем файл с диска (не упадёт, если файла нет)
    delete_metadata(filename)             # удаляем запись из БД
    logging.info(f'Изображение {filename} удалено')

    return redirect(url_for('images_list', page=page))

@app.get('/images-list')
def images_list():
    page= request.args.get('page', 1, type=int)
    per_page= 10
    offset= (page-1) * per_page
    total = get_count_images()
    rows = get_images(per_page=per_page,offset=offset)
    images = []
    for row in rows:
        images.append(
            {
                'id':row[0],
                'filename':row[1],
                'original_name':row[2],
                'size':row[3],
                'upload_time':row[4],
                'file_type':row[5],
                'url': url_for('get_image',filename=row[1])
            }
        )
    total_pages = (total+per_page-1)//per_page
    return render_template(
        template_name_or_list= 'images_list.html',
        images=images,
        page=page,
        total_pages=total_pages,
    )
@app.get('/users/<string:name>')
def get_user(name):
    return f'Hello {name}'

@app.get('/images/<path:filename>')
def get_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000,debug=True)


from flask import Flask,render_template,jsonify,request,send_from_directory,url_for
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge
import logging
import uuid
import os
from io import BytesIO
from pathlib import Path

from database.repository import save_metadata

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
    datefmt='%Y-%M-%D %H:%M:%S',
    encoding='utf-8'
)


def detect_image_extension(file_data: bytes):
    try:
        with Image.open(BytesIO(file_data)) as image:
            image.verify()

            return ALLOWED_IMAGE_FORMATS.get(image.format)
    except (UnidentifiedImageError,OSError):
            return None

@app.get("/")
def home():
    return render_template("index.html")


@app.get("/upload")
def upload_page():
    return render_template("upload.html")

@app.get('/images')
def images_page():
    images=[]

    for image_path in sorted(IMAGES_DIR.iterdir(), key=lambda path:path.stat().st_mtime, reverse=True):
        if not image_path.is_file():
            continue

        relative_url=url_for('get_image',filename=image_path.name)
        full_url=request.host_url.rstrip('/') + relative_url

        images.append(
            {
            'name':image_path.name,
            'relative_url':relative_url,
            'full_url':full_url,
            }
        )

    return render_template( template_name_or_list= 'images.html',images=Image)

@app.post('/upload')
def upload_image():
    uploaded_file = request.files.get('image')
    print(uploaded_file)
    if uploaded_file is None:
        logging.warning('Ошибка: файл image не найден в запросе')
        return jsonify({
            'error':'Файл не найден. Поле формы должно называться image'
        })

        original_filename= upload_file.filename or 'unknown'

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

@app.get('/users/<string:name>')
def get_user(name):
    return f'Hello {name}'

@app.get('/images/<path:filename>')
def get_image(filename):
    return send_from_directory(IMAGE_DIR, filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000,debug=True)


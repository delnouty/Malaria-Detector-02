from flask import Flask
import os
from .routes import init_routes

# Дефинирование базового пути проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Определение путей для загрузок и статических файлов
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                static_url_path='/static')
    
    # Конфигурация
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
    app.secret_key = 'your-secret-key-here'

    # Создание необходимых директорий при запуске
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(STATIC_FOLDER, exist_ok=True)

    # Инициализация маршрутов
    init_routes(app)

    return app

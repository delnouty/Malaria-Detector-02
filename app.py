from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Получить порт из переменных окружения или использовать 5000 по умолчанию
    port = int(os.environ.get('PORT', 5000))
    
    # Прослушивать все интерфейсы (0.0.0.0) для Azure
    app.run(host='0.0.0.0', port=port, debug=True)

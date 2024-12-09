# Используем официальный образ Python в качестве базового образа
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Обновление pip до последней версии
RUN python -m pip install --upgrade pip

# Копируем файл requirements.txt и устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в рабочую директорию
COPY . .

# Устанавливаем переменную окружения для Flask
ENV FLASK_APP=app.py

# Открываем порт 5000 для внешнего доступа
EXPOSE 5000

# Команда для запуска Flask приложения
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

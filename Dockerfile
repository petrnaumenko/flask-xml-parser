# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем sqlite3 для выполнения миграций
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY ./app /app

# Копируем миграции из уровня выше
COPY ./migrations /migrations

# Создаем папку instance, если её нет
RUN mkdir -p /app/instance

# Инициализация базы данных
RUN sqlite3 /app/instance/database.db < /migrations/init_db.sql

# Указываем порт, который будет использовать приложение
EXPOSE 5000

# Команда для запуска приложения
CMD ["flask", "run", "--host=0.0.0.0"]
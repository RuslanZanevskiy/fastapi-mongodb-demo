# Используем официальный базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --default-timeout=30 --no-cache-dir -r requirements.txt

# Копируем остальной код приложения
COPY . .

# Даем права на выполнение нашему стартовому скрипту
RUN chmod +x ./start.sh

# Указываем стартовый скрипт как команду по умолчанию
CMD ["./start.sh"]

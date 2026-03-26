# Используем официальный образ
FROM apache/airflow:2.10.2-python3.12

# Переключаемся на root для установки системных зависимостей
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Возвращаемся на пользователя airflow
USER airflow

ARG CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.12.txt"
# Копируем файл зависимостей в корень контейнера
COPY requirements.txt /requirements.txt

# Устанавливаем зависимости (БЕЗ флага --user)
# Мы просто обновляем текущее виртуальное окружение Airflow
RUN pip install --no-cache-dir -r /requirements.txt

# Указываем пути для поиска твоих модулей (папки services, training и т.д.)
ENV PYTHONPATH="/opt/airflow"

WORKDIR /opt/airflow
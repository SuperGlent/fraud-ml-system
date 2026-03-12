# Используем официальный образ Airflow с Python 3.12
FROM apache/airflow:2.10.2-python3.12

# Переключаемся на root, чтобы установить системные зависимости
USER root

# Устанавливаем git и библиотеки для работы с Postgres, если нужно
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Переключаемся обратно на пользователя airflow
USER airflow
# Добавляем пути к бинарникам и твоему коду
ENV PATH="${PATH}:/home/airflow/.local/bin"
ENV PYTHONPATH="/opt/airflow"
# Копируем requirements.txt
# Важно: путь должен быть доступен из контекста сборки (корня проекта)
COPY requirements.txt /requirements.txt

# Устанавливаем зависимости из твоего файла
# --no-cache-dir экономит место в образе
RUN pip install --no-cache-dir "apache-airflow[docker,postgres,celery]" -r /requirements.txt

# Копируем DAGs (хотя лучше прокидывать их через volumes в docker-compose для разработки)
# COPY ./dags /opt/airflow/dags

# Устанавливаем рабочую директорию
WORKDIR /opt/airflow
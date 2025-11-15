# API-сервис для вопросов и ответов: fastapi_tz
# Тестовое задание на fastapi с использованием postgresql
# Этапы запуска проекта:
# 1) Клонируем репозиторий с проектом: 
#  git clone https://github.com/Maksim-Borisov7/fastapi_tz
#  И переходим в папку командой: cd fastapi_tz
# 2) Запуск проекта: Создайте файл .env в папке fastapi_tz
#  Скопируйте содержимое папки .env.example в .env
#  Далее в терминале прописываем: docker compose up -d
#  Затем: docker exec -it fastapi_tz alembic upgrade head

# 3) Вставляем в браузер ссылку на swagger: http://localhost:8000/docs
# 4) Работа с PostgreSQL: docker exec -it psgr psql -U postgres -d postgres
# 5) Остановка проекта: docker compose down

Находясь в папке infra, выполните команду docker-compose up. При выполнении этой команды wконтейнер frontend, описанный в docker-compose.yml, подготовит файлы, необходимые для работы фронтенд-приложения, а затем прекратит свою работу.

По адресу http://localhost изучите фронтенд веб-приложения, а по адресу http://localhost/api/docs/ — спецификацию API.


python -m venv venv
source venv/Scripts/activate

python -m pip install --upgrade pip

pip freeze > requirements.txt


cd backend
django-admin startproject foodgram .
python manage.py startapp api

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

python manage.py loaddata data/ingredients.json
python manage.py makemigrations


foodgramsm.hopto.org
alexyssm

cd frontend
docker build -t alexyssm/foodgram_frontend .
cd ../backend
docker build -t alexyssm/foodgram_backend .
cd ../gateway
docker build -t alexyssm/foodgram_gateway .

docker login
docker push alexyssm/foodgram_frontend
docker push alexyssm/foodgram_backend
docker push alexyssm/foodgram_gateway

docker compose -f docker-compose.production.yml up
docker compose -f docker-compose.production.yml up -d

# Остановите все контейнеры
docker-compose -f docker-compose.production.yml down

# Удалите volume с данными PostgreSQL
docker volume rm foodgram_pg_data

# Или удалите все volumes проекта
docker-compose -f docker-compose.production.yml down -v

# Запустите заново
docker-compose -f docker-compose.production.yml up
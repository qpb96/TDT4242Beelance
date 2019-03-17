release: pip install -r requirements.txt
release: python manage.py makemigrations
release: python manage.py migrate
release: python manage.py runjobs clean_active_promotions
web: python manage.py runserver 0.0.0.0:$PORT

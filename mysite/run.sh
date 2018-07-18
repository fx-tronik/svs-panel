. /home/yason/workspace/django/venv/bin/activate
cd /home/yason/workspace/django/mysite
gnome-terminal --window-with-profile=shell -e "celery -A mysite beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler"
gnome-terminal --window-with-profile=shell -e "celery worker -A mysite -l info --without-mingle"
gnome-terminal --window-with-profile=shell -e "python manage.py runserver"

python -m venv venv
. venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
touch apps/users/tests/__init__.py
python manage.py test apps.users -v2
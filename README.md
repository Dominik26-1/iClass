# iClass

Step to run Django server:

1. install python at least 3.9
2. install pip (upgrade to at least 23.0.1)
3. clone project from git
4. create and set virtual environment with python at least 3.9
5. turn on environment (./venv/Scripts/activate)
6. install python packages from requirements.txt:  
pip install -r requirements.txt
7. set up postgresql database with default settings:

'NAME': 'iClass',
'USER': 'postgres',
'PASSWORD': 'postgres',
'HOST': 'localhost',
'PORT': '5432'

8. python manage.py makemigrations
9. python manage.py migrate
10.python manage.py runserver
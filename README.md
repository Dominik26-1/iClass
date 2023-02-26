# iClass

Step to run Django server:

1. install python

2. instal pip 
3. install python packages from requirements.txt:  
pip install -r requirements.txt
4. set up postgresql database with default settings:

'NAME': 'iClass',
'USER': 'postgres',
'PASSWORD': 'postgres',
'HOST': 'localhost',
'PORT': '5432'

5. python manage.py makemigrations
6. python manage.py migrate
7. python manage.py runserver
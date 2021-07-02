# financeeper-Backend

clone this repository

# Database setup
create a database in postgres

In project settings.py file in Databases section

'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
    
 Here in this default section give your created Database Name, Username of postgres,
 Password and Host and Port(same if we are running in local)
 
 # Migrations commad
 
 After that run there two important commands
 
 python manage.py makemigrations,
 python manage.py migrate
 
 # Create Super User
 python manage.py createsuperuser
 
 # After the success above all commads 
 # To run server
 
 python manage.py runserver

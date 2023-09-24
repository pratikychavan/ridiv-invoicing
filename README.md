# ridiv-invoicing

Steps to run in virtualenv
1. activate your virtualenv and install requirements.txt using "pip install -r requirements.txt"
2. run migrations using "python manage.py migrate"
3. run server using "python manage.py runserver"

Steps to run in docker-assuming you have make, docker and docker-compose installed
1. run "make up-inv"
2. run "make inv"
3. run "make local"

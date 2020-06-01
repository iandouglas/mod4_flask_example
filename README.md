1. set up virtualenv or pipenv, activate the virtual environment
2. pip install -r requirements.txt
3. create a postgresql database:
    ```
    $ psql
    # create database wordcount_dev;
    ```
4. set up the project database:
    ```
    python manage.py db init
    python manage.py db migrate
    python manage.py db upgrade
    ```
5. run the server
    ```
    python run.py
    ```
6. run tests:
    ```
    nosetests
    ```
7. Buy Ian a Diet Dr Pepper
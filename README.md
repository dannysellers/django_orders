django_orders
=============

Overview
--------

Order tracker (see flask_orders and order_tracker repos) implemented in Django.

Usage
-----
To create a database, run

    python managey.py syncdb

Afterwards, you can use load_accts.py or populate.py to load accounts from a .csv (account_list.csv
by default) and / or populate the database with randomly generated accounts and items.

After populating the database, start the server with

    python manage.py runserver

and navigate to http://localhost:8000 .
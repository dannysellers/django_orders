django_orders
=============

Overview
--------

Order tracker (see flask_orders and order_tracker repos) implemented in Django.

Usage
-----
On first run, run
    
    python manage.py syncdb

to create a database. After that, you can use load_accts to load a .csv (account_list.csv) containing Name (str), Acct (5-digit int), and Date Created (MM/DD/YYYY) columns. 

To start the server, run

    python manage.py runserver

and navigate to http://localhost:8000 .
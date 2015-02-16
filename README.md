django_orders
=============

Overview
--------

This tool is intended for tracking accounts and inventory for customers of an order fulfillment business, for example, an intermediary who receives goods from a supplier and prepares them for shipment to a Fulfillment by Amazon warehouse, or for shipment to customers.

Getting Started
---------------
After downloading the repo, install required packages from requirements.txt:

    pip install -r requirements.txt

To create a database, run

    ./manage.py syncdb

followed by a

    ./manage.py migrate tracker

and finally a

    ./manage.py runserver

to start it up.

load_accts.py and populate.py exist to import data into the database, though neither are up to date.

The .csv where accounts are loaded from must have the following columns (in no particular order): "Names", "Acct", and "Date Created". The .csv I had to load from had dates that required fixing, but ultimately, Django requires dates be formatted as YYYY-MM-DD, so you may have to modify that script to match the data.

Usage
-----

django_orders
=============

Overview
--------

This tool was intended for tracking accounts and inventory for customers of an order fulfillment business, for example, a middleman who receives goods from a supplier and prepares them for shipment to a Fulfillment by Amazon warehouse, or for shipment to customers.

Usage
-----
After downloading the repo, install packages from requirements.txt, including _Django (1.5.4)_, _South (1.0.1)_, _pytz (2014.10)_, and _wsgiref (0.1.2)_:

    pip install -r requirements.txt

To create a database, run

    python managey.py syncdb

At this point, you can start the server (manage.py runserver) and begin playing around, and though there will be no data besides the single superuser, customers and inventory can be added from within the interface (after logging in).

The database can be populated by running load_accts.py or populate.py to load accounts from a .csv (account_list.csv by default), or to populate the database with randomly generated accounts and items.

The .csv from which accounts are loaded must have the following columns (in no particular order): "Names", "Acct", and "Date Created". The .csv I had to load from had dates that required fixing, but ultimately, Django requires dates be formatted as YYYY-MM-DD, so you may have to modify that script to match the data.

Context
-------
This tool was created for my employer, who deal primarily in postal mail, but have a fledgling division to provide inspection and repackaging of inventory for online sellers. Ultimately, they were not interested in this tool, both because it is standalone and because it is written in a different language than any of their internal tools. As a result, I have ceased active development on this project.

This was under development from mid-November to the end of December 2014.
Meal Delivery

Author: Anu B Nair <anubnair90@gmail.com>

About:
------

This application is to manage the meal delivery of staff....

Installation:
-------------

$sudo ./install.sh

How to use:
-----------

Terminal 1: 
------------
$python server.py   

Terminal 2:
------------
Running client for API validation:

Add Menu:
---------
python client.py -m "{'item_name':'rice', 'price':10, 'category': 'VEG', 'event': 'add'}"

response: 200 {"menu": {"status": "success", "event": "add"}}

Remove menu:
------------
python2 client.py -m "{'item_name':'rice', 'price':10, 'category': 'VEG', 'event': 'remove'}"

response: 200 {"menu": {"status": "success", "event": "remove"}}

Update menu:
------------
python2 client.py -m "{'item_name':'rice', 'price':10, 'category': 'VEG', 'event': 'edit', 'old_item_name': 'rice'}"

response: 200 {"menu": {"status": "success", "event": "edit"}}

Add Team:
---------

python2 client.py -t "{'team_name':'data_science', 'event': 'add'}"

response: 200 {"team": {"status": "success", "event": "add"}}

Delete Team:
------------

python2 client.py -t "{'team_name':'data_science', 'event': 'delete'}"

response: 200 {"team": {"status": "success", "event": "delete"}}
Sample Nose Test:
------------------
$cd tests
$nosetests .


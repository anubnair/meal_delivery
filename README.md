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


Add Employee:
-------------
python2 client.py -e "{'emp_name':'anu', 'food_tag': 'VEG', 'team_name': 'data_science', 'team_id':1, 'event': 'add'}"

response 200 {"employee": {"status": "success", "event": "add"}}

Delete Employee:
---------------
python2 client.py -e "{'emp_name':'anu', 'food_tag': 'VEG', 'team_name': 'data_science', 'team_id':1, 'event': 'delete'}"

response 200 {"employee": {"status": "success", "event": "delete"}}

Edit Employee:
-------------
python2 client.py -e "{'emp_name':'anu', 'food_tag': 'VEG', 'team_name': 'data_science', 'team_id':1, 'event': 'edit', 'old_team_name': 'data_science'}"

response 200 {"employee": {"status": "success", "event": "edit"}}

Sample Nose Test:
------------------
$cd tests
$nosetests .


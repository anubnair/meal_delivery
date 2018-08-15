Meal Delivery

Author: Anu B Nair <anubnair90@gmail.com>

About:
------


+-----------------------------+     Response         +-----------------------+
|        WebServer(Tornado)   <------------------+   |         Client        |
|                             +----------------->    |                       |
+-----^-----------------------+     Request          +-----------------------+
      ||
      ||
      ||
      ||
      ||
      ||
+------v--------------+
|                     |
|      Mysql(DB)      |
+---------------------+



----------------------------------------------
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
python2 client.py -m "{'item_name':'rice', 'price':10, 'category': 'VEG', 'event': 'add'}"

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

Add restaurant:
---------------
python2 client.py -r "{'res_name':'Anu', 'food_tag': 'VEG', 'menu_id':4, 'event': 'add'}"

response 200 {"restaurant": {"status": "success", "event": "add"}}

Delete restaurant:
------------------
python2 client.py -r "{'res_name':'Anu', 'food_tag': 'VEG', 'menu_id':4, 'event': 'delete'}"

response 200 {"restaurant": {"status": "success", "event": "delete"}}

Edit restaurant:
---------------
python2 client.py -r "{'res_name':'Anu', 'food_tag': 'VEG', 'menu_id':4, 'event': 'edit', 'old_res_name': 'Anu'}"
    
response 200 {"restaurant": {"status": "success", "event": "edit"}}

Random Lunch:
-------------
python2 client.py -l "{'team_id':1}"

response 200 {"random_lunch": {"status": "success", "result": [[4, "Anu", "VEG", 4], [5, "Anoop", "VEG", 4]]}}

Paid Lunch:
-----------
python2 client.py -p "{'team_id':1, 'total_budget': 10}"

response 200 {"random_lunch": {"status": "success", "result": {"menu": [[4, "rice", 10, "VEG"], [5, "rice", 10, "VEG"], [6, "rice", 10, "VEG"], [7, "rice", 10, "VEG"], [8, "rice", 10, "VEG"], [9, "rice", 10, "VEG"], [10, "rice", 10, "VEG"], [11, "rice", 10, "VEG"], [12, "rice", 10, "VEG"], [13, "rice", 10, "VEG"], [14, "rice", 10, "VEG"], [15, "rice", 10, "VEG"], [16, "rice", 10, "VEG"], [17, "rice", 10, "VEG"], [18, "rice", 10, "VEG"], [19, "rice", 10, "VEG"]], "restaurant": [[4, "Anu", "VEG", 4], [5, "Anoop", "VEG", 4]]}}}

Get Teams:
----------
python2 client.py --get_teams "{'event': 'get_teams'}"

response 200 {"get_teams": {"status": "success", "result": [[1, "data_science"]]}}`

Get Employees:
-------------
python2 client.py --get_employees "{'event': 'get_employees'}"

response 200 {"get_employees": {"status": "success", "result": [[2, "anu", "VEG", "data_science", 1], [3, "anp", "VEG", "data_science", 1], [4, "deepu", "VEG", "data_science", 1], [5, "namratha", "VEGAN", "data_science", 1]]}}

Get Restaurants:
----------------

python2 client.py --get_restaurants "{'event': 'get_restaurants'}"

response 200 {"get_restaurants": {"status": "success", "result": [[4, "Anu", "VEG", 4], [5, "Anoop", "VEG", 4]]}}


Sample Nose Test:
------------------
$cd tests
$nosetests .

Create DB:
----------
mysql -u root mydb < db_skel.sql 

import httplib
import urllib
import json
import optparse

params = urllib.urlencode({'username': 'admin', 'password': 'iamadmin'})

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/plain"}
conn = httplib.HTTPConnection("localhost", 8888)

conn.request("POST", "/", params, headers)
response = conn.getresponse()
key = json.loads(response.read())['key']


def menu(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    if arg['event'] == 'edit':
        params = urllib.urlencode({'key': key, 'item_name': arg['item_name'],
                                   'price': arg['price'],
                                   'category': arg['category'],
                                   'old_item_name': arg['old_item_name'],
                                   'event': arg['event']})
    else:
        params = urllib.urlencode({'key': key, 'item_name': arg['item_name'],
                                   'price': arg['price'],
                                   'category': arg['category'],
                                   'event': arg['event']})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/menu", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def team(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    params = urllib.urlencode({'key': key, 'team_name': arg['team_name'],
                                   'event': arg['event']})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/team", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def employee(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    if arg['event'] == 'edit':
        params = urllib.urlencode({'key': key, 'emp_name': arg['emp_name'],
                                   'food_tag': arg['food_tag'],
                                   'team_name': arg['team_name'],
                                   'team_id': arg['team_id'],
                                   'old_team_name': arg['old_team_name'],
                                   'event': arg['event']})
    else:
        params = urllib.urlencode({'key': key, 'emp_name': arg['emp_name'],
                                   'food_tag': arg['food_tag'],
                                   'team_name': arg['team_name'],
                                   'team_id': arg['team_id'],
                                   'event': arg['event']})

    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/employee", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def restaurant(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    if arg['event'] == 'edit':
        params = urllib.urlencode({'key': key, 'res_name': arg['res_name'],
                                   'category': arg['food_tag'],
                                   'menu_id': arg['menu_id'],
                                   'old_res_name': arg['old_res_name'],
                                   'event': arg['event']})
    else:
        params = urllib.urlencode({'key': key, 'res_name': arg['res_name'],
                                   'category': arg['food_tag'],
                                   'menu_id': arg['menu_id'],
                                   'event': arg['event']})

    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/restaurant", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def random_lunch(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    params = urllib.urlencode({'key': key, 'team_id': arg['team_id']})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/random_lunch", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def paid_lunch(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    params = urllib.urlencode({'key': key, 'team_id': arg['team_id'],
                                'total_budget': arg['total_budget']})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("POST", "/paid_lunch", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def get_teams(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    params = urllib.urlencode({'key': key})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("GET", "/get_teams", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def get_employees(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    params = urllib.urlencode({'key': key})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("GET", "/get_employees", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())


def get_restaurants(arg):
    json_acceptable_string = arg.replace("'", "\"")
    arg = json.loads(json_acceptable_string)
    params = urllib.urlencode({'key': key})
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}
    conn = httplib.HTTPConnection("localhost", 8888)
    conn.request("GET", "/get_restaurants", params, headers)
    response = conn.getresponse()
    print(response.status, response.read())

if __name__ == '__main__':

    parser = optparse.OptionParser(usage="usage: %prog [options] filename",
                                   version="%prog 1.0")
    parser.add_option('-m', '--menu',
                      dest="menu",
                      help='add /update/ delete menu',)

    parser.add_option('-t', '--team',
                      dest="team",
                      help='add / delete team',)

    parser.add_option('-e', '--employee',
                      dest="employee",
                      help='add / update, delete team',)

    parser.add_option('-r', '--restaurant',
                      dest="restaurant",
                      help='add /update/ delete restaurant',)

    parser.add_option('-l', '--random_lunch',
                      dest="random_lunch",
                      help='Random Lunch for multiple employees',)

    parser.add_option('-p', '--paid_lunch',
                      dest="paid_lunch",
                      help='Paid Lunch for multiple employees',)

    parser.add_option('--get_teams',
                      dest="get_teams",
                      help='Get all Teams',)

    parser.add_option('--get_employees',
                      dest="get_employees",
                      help='Get all Employees',)

    parser.add_option('--get_restaurants',
                      dest="get_restaurants",
                      help='Get all Restaurants',)

    (options, args) = parser.parse_args()

    if options.menu:
        menu(options.menu)
    if options.team:
        team(options.team)
    if options.employee:
        employee(options.employee)
    if options.restaurant:
        restaurant(options.restaurant)
    if options.random_lunch:
        random_lunch(options.random_lunch)
    if options.paid_lunch:
        paid_lunch(options.paid_lunch)
    if options.get_teams:
        get_teams(options.get_teams)
    if options.get_employees:
        get_employees(options.get_employees)
    if options.get_restaurants:
        get_restaurants(options.get_restaurants)

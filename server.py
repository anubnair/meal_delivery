# -*- coding: utf-8; -*-
#
# Meal delivery is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Meal delivery is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with News Parsing.  If not, see <http://www.gnu.org/licenses/>.
#
# @author : Anu B Nair <anubnair90@gmail.com>

import tornado.autoreload
import tornado.ioloop
import tornado.web
import tornado.httpserver
from tornado import gen

import jwt
import ssl
import datetime
import json
import utils
import settings
#from bson import json_util


def authenticate(func):
    """
    Basic authentication
    """
    def inner(self):

        username = self.get_argument('username')
        password = self.get_argument('password')

        if username == 'admin' and password == 'iamadmin':
            encoded = jwt.encode(
                    {username: password,
                     'exp': (datetime.datetime.utcnow()
                             + datetime.timedelta(seconds=1000000))},
                    'secret', algorithm='HS256'
            )

            encoded = {'error': None, 'key': encoded.decode("utf-8")}
            func(self, encoded)
        else:
            func(self, {'error': 'Invalid username/Password',
                 'key': None})
    return inner


def authentication_required(func):
    """
    Check authentication
    """
    def inner(self):

        key = self.get_argument('key')
        try:
            decoded = jwt.decode(key, 'secret')
        except jwt.ExpiredSignatureError:
            decoded = {'error': 'ExpiredSignatureError'}
            self.clear()
            self.set_status(401)
            self.finish(json.dumps(decoded))
            return
        except jwt.InvalidTokenError:
            decoded = {'error': 'InvalidTokenError'}
            self.clear()
            self.set_status(401)
            self.finish(json.dumps(decoded))
            return
        func(self, decoded)

    return inner


class MainHandler(tornado.web.RequestHandler):
    @authenticate
    def post(self, encoded):
        self.write(json.dumps(encoded))


class JsonObject:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


def fetch_all_restaurants(db):
    """
    Get all restaurant details from the DB
    Args:
        db: DB object
    Returns:
        results: all restaurants
    """
    return {}

def add_menu(item_name, price, category, db):
    """
    add new menu to DB
    Args:
        item_name: item name
        price: price in SGD
        category: category of food (VEG, VEGAN, MEAT, FISH, CHICKEN)
        db: db object
    Returns:
        data: curresponding result
    """
    try:
        return_data = {}
        query = ('INSERT INTO menu_table (menu_id, item_name, price,' + \
                                 'category) ' + \
                                 'VALUES (%s, "%s", "%s", "%s")' \
                                    % ("default", item_name, str(price), \
                                        category)
                                )
        print(query)
        utils.write_to_mysql(db, query)
        return_data = {
                        "menu": {
                                    "event": "add",
                                    "status":"success"
                                }
                    }
        print(return_data)
    except Exception as e:
        return_data = {
                        "menu": {
                                    "event": "add",
                                    "status":"fail"
                                }
                    }
    return return_data


def edit_menu(item_name, old_item_name, price, category, db):
    """
    add new menu to DB
    Args:
        item_name: item name
        price: price in SGD
        category: category of food (VEG, VEGAN, MEAT, FISH, CHICKEN)
        db: db object
    Returns:
        data: curresponding result
    """
    try:
        return_data = {}
        query = ("UPDATE menu_table SET item_name='%s', price=%s,"
                                % (item_name, str(price))
                                + "category='%s' " % (category)
                                + "WHERE item_name = '%s'" % (old_item_name))

        print(query)
        utils.write_to_mysql(db, query)
        return_data = {
                        "menu": {
                                    "event": "update",
                                    "status":"success"
                                }
                    }
    except Exception as e:
        return_data = {
                        "menu": {
                                    "event": "update",
                                    "status":"fail"
                                }
                    }
    return return_data

def remove_menu(item_name, price, category, db):
    """
    add new menu to DB
    Args:
        item_name: item name
        price: price in SGD
        category: category of food (VEG, VEGAN, MEAT, FISH, CHICKEN)
        db: db object
    Returns:
        data: curresponding result
    """
    try:
        return_data = {}
        query = ("DELETE from menu_table WHERE item_name='%s' AND price=%s" \
    			     % (str(item_name), str(price)) \
                                 + " AND category='%s'; " % (str(category)))
        print(query)
        utils.write_to_mysql(db, query)
        return_data = {
                        "menu": {
                                    "event": "remove",
                                    "status":"success"
                                }
                    }
    except Exception as e:
        return_data = {
                        "menu": {
                                    "event": "remove",
                                    "status":"fail"
                            }
                    }
    return return_data

def add_or_remove_team(team_name, event, db):
    """
    add new Tean to DB
    Args:
        team_name: team name
        event: add or remove a team
        db: db object
    Returns:
        data: curresponding result
    """
    try:
        return_data = {}
        if event == 'add':
            query = ("INSERT INTO team_table (team_id, team_name) "+ \
    			                 'VALUES (%s, "%s")' \
                                 %  ("default", team_name)
                    )
            print(query)
            utils.write_to_mysql(db, query)
            return_data = {
                            "team": {
                                        "event": event,
                                        "status":"success"
                                    }
                        }
        if event == 'delete':
            query = ("DELETE from team_table WHERE team_name='%s'; "
                        % (str(team_name)))

            print(query)
            utils.write_to_mysql(db, query)
            return_data = {
                            "team": {
                                        "event": event,
                                        "status":"success"
                                    }
                        }
    except Exception as e:
        return_data = {
                        "team": {
                                    "event": event,
                                    "status":"fail"
                                }
                    }
    return return_data


class Menu(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        """
        API to add/remove/edit the Menu
        """
        item_name = self.get_argument('item_name')
        price = self.get_argument('price')
        category = self.get_argument('category')
        event = self.get_argument('event')

        if event == 'add':
            out = add_menu(item_name, price, category,
                           self.settings['db'])
        elif event == 'remove':
            out = remove_menu(item_name, price, category,
                           self.settings['db'])
        elif event == 'edit':
            old_item_name = self.get_argument('old_item_name')
            out = edit_menu(item_name, old_item_name,
                            price, category,
                            self.settings['db'])
        if out['menu']['status'] == 'fail':
            self.set_statusmenu(400)
            self.finish(out)
        else:
            self.write(json.dumps(out))
            self.finish()


class Team(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        """
        API to add/remove a new Team
        """
        team_name = self.get_argument('team_name')
        event = self.get_argument('event')

        out = add_or_remove_team(team_name, event,
                           self.settings['db'])

        if out['team']['status'] == 'fail':
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(out))
            self.finish()


def update_emp_information(emp_name, food_tag,
                            team_id, team_name, event,
                            db, old_team_name=None):
    """
    Update employee info to DB
    Args:
        emp_name: employee name
        food_tag: food category of an employee
        team_id: team_id of the Employee
        team_name: team name
        event: add,remove,edit information of employee
        db: db object
    Returns:
        data: curresponding result
    """
    try:
        return_data = {}

        if event == 'add':
            query = ("INSERT INTO employee_table (id, emp_name, food_tag," +
                                "team_id, team_name) "+ \
    			                 'VALUES (%s, "%s", "%s", %s, "%s")' \
                                 %  ("default", emp_name,
                                     food_tag, team_id, team_name)
                    )
            print(query)
            utils.write_to_mysql(db, query)
            return_data = {
                            "employee": {
                                        "event": event,
                                        "status":"success"
                                    }
                        }
        if event == 'delete':
            query = ("DELETE from employee_table WHERE emp_name='%s'; "
                        % (str(emp_name)))

            print(query)
            utils.write_to_mysql(db, query)
            return_data = {
                            "employee": {
                                        "event": event,
                                        "status":"success"
                                    }
                        }
        if event == 'edit':
            query = ("UPDATE employee_table SET emp_name='%s', food_tag='%s',"
                                % (emp_name, food_tag)
                                + "team_name='%s', " % (team_name)
                                + "team_id=%s " % (team_id)
                                + "WHERE    team_name = '%s'" % (old_team_name))

            print(query)
            utils.write_to_mysql(db, query)
            return_data = {
                            "employee": {
                                        "event": event,
                                        "status":"success"
                                    }
                        }
    except Exception as e:
        return_data = {
                        "employee": {
                                    "event": event,
                                    "status":"fail"
                                }
                    }
    return return_data



def update_res_information(res_name, category,
                            menu_id, event,
                            db, old_res_name=None):
    """
    Update restaurant info to DB
    Args:
        res_name: restaurant name
        category: food category of a restaurant
        menu_id: menu id
        event: add,remove,edit restaurant
        db: db object
        old_res_name: old restaurant name(for update)
    Returns:
        data: curresponding result
    """
    try:
        return_data = {}

        if event == 'add':
            query = ("INSERT INTO restaurant_table (res_id, res_name, " + \
                                "category, menu_id) " + \
    			                 'VALUES (%s, "%s", "%s", "%s")' \
                                 %  ("default", res_name,
                                     category, menu_id)
                    )
            print(query)
            utils.write_to_mysql(db, query)
            return_data = {
                            "restaurant": {
                                        "event": event,
                                        "status":"success"
                                    }
                        }
        if event == 'delete':
            query = ("DELETE from restaurant_table WHERE res_name='%s'; "
                        % (str(res_name)))

            print(query)
            utils.write_to_mysql(db, query)
            return_data = {
                            "restaurant": {
                                        "event": event,
                                        "status":"success"
                                    }
                        }
        if event == 'edit':
            query = ("UPDATE restaurant_table SET res_name='%s', category='%s',"
                                % (res_name, category)
                                + "menu_id=%s " % (menu_id)
                                + "WHERE res_name = '%s'" % (old_res_name))

            print(query)
            utils.write_to_mysql(db, query)
            return_data = {
                            "restaurant": {
                                        "event": event,
                                        "status":"success"
                                    }
                        }
    except Exception as e:
        return_data = {
                        "restaurant": {
                                    "event": event,
                                    "status":"fail"
                                }
                    }
    return return_data


class Employee(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        """
        API to add/remove/edit employee information
        """
        emp_name = self.get_argument('emp_name')
        food_tag = self.get_argument('food_tag')
        team_id = self.get_argument('team_id')
        team_name = self.get_argument('team_name')
        event = self.get_argument('event')

        if event == 'edit':
            old_team_name = self.get_argument('old_team_name')
            out = update_emp_information(emp_name, food_tag,
                                        team_id, team_name, event,
                                        self.settings['db'],old_team_name)
        else:
            out = update_emp_information(emp_name, food_tag,
                                        team_id, team_name, event,
                                        self.settings['db'])

        if out['employee']['status'] == 'fail':
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(out))
            self.finish()


class Restaurant(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        """
        API to add/remove/edit restaurant
        """
        res_name = self.get_argument('res_name')
        category = self.get_argument('category')
        menu_id = self.get_argument('menu_id')
        event = self.get_argument('event')

        if event == 'edit':
            old_res_name = self.get_argument('old_res_name')
            out = update_res_information(res_name, category,
                                        menu_id, event,
                                        self.settings['db'],old_res_name)
        else:
            out = update_res_information(res_name, category,
                                        menu_id, event,
                                        self.settings['db'])

        if out['restaurant']['status'] == 'fail':
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(out))
            self.finish()


class Random_lunch(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        """
        API to schedule a “Random Lunch” for multiple employees
        """
        team_id = self.get_argument('team_id')
        # get all employee with the team_id
        query = ("SELECT * from employee_table "
                                + "WHERE team_id = %s" % (team_id))
        db = self.settings['db']
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        if not result:
            return_data = {
                            "random_lunch": {
                                        "result": None,
                                        "status":"fail"
                                    }
                        }
        else:
            category_list =[]
            for res in result:
                if res[2] not in category_list:
                    category_list.append(res[2])
            query = ("SELECT * from restaurant_table WHERE")
            cat_count = 0
            for cat in category_list:
                if cat_count:
                    query += " or category =  '%s'" % (cat)
                else:
                    query += " category = '%s'" % (cat)
                cat_count += 1

            print(query)
            db = self.settings['db']
            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            return_data = {
                        "random_lunch": {
                                    "result": result,
                                    "status":"success"
                                }
                    }

        if return_data['random_lunch']['status'] == 'fail':
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(return_data))
            self.finish()

class Paid_lunch(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        """
        API to schedule a “Paid Lunch” for multiple employees
        """

        team_id = self.get_argument('team_id')
        total_budget = self.get_argument('total_budget')
        # get all employee with the team_id
        query = ("SELECT * from employee_table "
                                + "WHERE team_id = %s" % (team_id))
        db = self.settings['db']
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        if not result:
            return_data = {
                            "paid_lunch": {
                                        "result": None,
                                        "status":"fail"
                                    }
                        }
        else:
            individual_price = int(total_budget)/len(result)
            category_list =[]
            for res in result:
                if res[2] not in category_list:
                    category_list.append(res[2])
            query = ("SELECT * from menu_table WHERE")
            cat_count = 0
            for cat in category_list:
                if cat_count:
                    query += " or category =  '%s'" % (cat)
                else:
                    query += " category = '%s'" % (cat)
                cat_count += 1

            query += " and price<=%s" % (individual_price)

            db = self.settings['db']
            cursor = db.cursor()
            cursor.execute(query)
            avail_menu = cursor.fetchall()

            list_menu_id = []
            for menu in avail_menu:
                list_menu_id.append(menu[0])
            string_menu_id = ','.join(str(v) for v in list_menu_id)
            # find available restaurant
            query = ("SELECT * from restaurant_table WHERE menu_id in (%s)"
                        % (string_menu_id))
            db = self.settings['db']
            cursor = db.cursor()
            cursor.execute(query)
            list_restaurant = cursor.fetchall()

            return_data = {
                        "random_lunch": {
                                    "result": {"menu": avail_menu,
                                                "restaurant": list_restaurant},
                                    "status":"success"
                                }
                    }

        if return_data['random_lunch']['status'] == 'fail':
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(return_data))
            self.finish()


class Get_Teams(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def get(self, decoded):
        """
        API to get Team details
        """
        query = ("SELECT * from team_table ")
        db = self.settings['db']
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            out = {
                            "get_teams": {
                                        "result": None,
                                        "status":"fail"
                                    }
                        }
        else:
            out = {
                            "get_teams": {
                                        "result": result,
                                        "status":"success"
                                    }
                        }
        if out['get_teams']['status'] == 'fail':
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(out))
            self.finish()


class Get_Employees(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def get(self, decoded):
        """
        API to get Team details
        """
        query = ("SELECT * from employee_table ")
        db = self.settings['db']
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            out = {
                            "get_employees": {
                                        "result": None,
                                        "status":"fail"
                                    }
                        }
        else:
            out = {
                            "get_employees": {
                                        "result": result,
                                        "status":"success"
                                    }
                        }
        if out['get_employees']['status'] == 'fail':
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(out))
            self.finish()


class Get_Restaurants(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def get(self, decoded):
        """
        API to get Team details
        """
        query = ("SELECT * from restaurant_table ")
        db = self.settings['db']
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            out = {
                            "get_restaurants": {
                                        "result": None,
                                        "status":"fail"
                                    }
                        }
        else:
            out = {
                            "get_restaurants": {
                                        "result": result,
                                        "status":"success"
                                    }
                        }
        if out['get_restaurants']['status'] == 'fail':
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(out))
            self.finish()


configuraion = utils.read_from_configuration('config.yaml')
db = utils.get_db_connection(configuraion)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/menu", Menu),
    (r"/team", Team),
    (r"/employee", Employee),
    (r"/restaurant", Restaurant),
    (r"/random_lunch", Random_lunch),
    (r"/paid_lunch", Paid_lunch),
    (r"/get_teams", Get_Teams),
    (r"/get_employees", Get_Employees),
    (r"/get_restaurants", Get_Restaurants),
], db=db)

if __name__ == "__main__":

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()

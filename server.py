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
from pymongo import MongoClient
from bson import json_util


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
        data_to_store = {}
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
        data_to_store = {}
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
        data_to_store = {}

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
        data_to_store = {}
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
            self.set_status(400)
            self.finish(out)
        else:
            self.write(json.dumps(out))
            self.finish


class Team(tornado.web.RequestHandler):
    @authentication_required
    @tornado.web.asynchronous
    @gen.engine
    def post(self, decoded):
        """
        API to add/remove a new Team
        """
        print("Came here")
        team_name = self.get_argument('team_name')
        event = self.get_argument('event')

        out = add_or_remove_team(team_name, event,
                           self.settings['db'])

        print(out)
        if out['team']['status'] == 'fail':
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
], db=db)

if __name__ == "__main__":

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
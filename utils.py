# -*- coding: utf-8; -*-
#

# This file is part of Mandriva Management Console (MMC).
#
# Meal delivery  is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Meal delivery  is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MMC.  If not, see <http://www.gnu.org/licenses/>.
#
# @author : Anu B Nair <anubnair90@gmail.com>

import yaml
import mysql.connector

def get_db_connection(configuraion):
    """
    Get Db connect string from the configuraion
    Args:
        configuraion (Dictionary): configuraion
    Returns:
        connect_string (string): DB connect string
    """

    connect_string = None
    if 'DB' in configuraion:
        for db in configuraion['DB']:
            user = db['user']
            password = db['password']
            host = db['host']
            db_name = db['db']
            port = db['port']
    else:
        print('No DB details in the configuraion')
        exit(1)

    mydb = mysql.connector.connect(
                    host=host,
                    user=user,
                    passwd=password,
                    port=port,
                    db=db_name
                    )

    return mydb

def write_to_mysql(mysql_obj, query):
    """ Write to mysql
        args    :   mysql object and query to execute"""

    try:
        print('Writing into MySQL...')
        cursor = mysql_obj.cursor()
        cursor.execute(query)
        mysql_obj.commit()
        cursor = mysql_obj.cursor()
        cursor.close()
    except Exception as err:
        print('Mysql write error : ' + str(err))
        raise Exception


def read_from_configuration(file_name):
    """
    Read from configuraion file
    Args:
        file_name (string): File name of the configuraion
    Returns:
        yaml_content (Dictionary): configuraion
    """

    with open(file_name, 'r') as yaml_fobj:
        yaml_content = yaml.load(yaml_fobj)

    return yaml_content


if __name__ == '__main__':
    configuraion = read_from_configuration('config.yaml')
    get_db_connection(configuraion)

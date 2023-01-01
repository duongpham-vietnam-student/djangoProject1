import time

from django.db import models
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import psycopg2
from psycopg2 import Error
from djangoProject1.common import *

# Create your models here.
# string, int, ...
class BOAUser():
    def __init__(self, id, username, password, email, usertype):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.type = usertype
        self.typefix = tranferUsertype(int(self.type))
BOAUsers = list()

def MigrateDataBOAUser():
    data = HookData("DATABASE")
    BOAUsers.clear()
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Executing a SQL query
        cursor.execute("select * from boauser")
        # Fetch result
        records = cursor.fetchall()
        # The function code
        for row in records:

            temp = BOAUser(row[0], row[1], row[2], row[3], row[4])
            BOAUsers.append(temp)
        return 1
    except (Exception, Error) as error:
        return 0
    finally:
        if (connection):
            cursor.close()
            connection.close()
def RequestAccount(command, dataset):
    data = HookData("DATABASE")
    if command == "i":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            print(connection)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            query = """insert into forgotrequest(email, ex, code)
                                   values (%s,%s,%s)"""
            cursor.execute(query, dataset)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
    elif command == "d":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            cursor.execute("delete from forgotrequest where email=%s", dataset)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
    elif command == "e":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor_e = connection.cursor()
            # Executing a SQL query
            cursor_e.execute("select * from forgotrequest")
            # Fetch result
            record_e = cursor_e.fetchall()
            # The function code
            for row in record_e:
                if dataset == row[0]:
                    return 1
            return 0
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor_e.close()
def ResetRequestAccount():
    data = HookData("DATABASE")
    now = time.time()
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        #Executing a SQL query
        query = """select * from forgotrequest"""
        cursor.execute(query)
        record = cursor.fetchall()
        # The function code
        for row in record:
            if now > int(row[1]) + 900:
                RequestAccount("d", row[0])
        return 1
    except (Exception, Error) as error:
        return 0
    finally:
        if (connection):
            cursor.close()
            connection.close()

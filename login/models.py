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
class BOAUser(): #tao class
    def __init__(self, id, username, password, email, usertype): #ham __init__ la ham khoi tao
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.type = usertype
        self.typefix = tranferUsertype(int(self.type))
#dung de lay thong tin tu database, bang boauser
BOAUsers = list() #tao doi tuong, list

#front end: username, password
#back end: lay het dataser, so sanh dua ket qua
# database: table
# back end: class
def MigrateDataBOAUser(): #lay data trong database
    data = HookData("DATABASE")
    BOAUsers.clear()
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        #bat ki ham nao tuong tac database deu phai co buoc connection va cursor, chi khac nhau phia duoi
        # Executing a SQL query
        cursor.execute("select * from boauser")
        #execute khac nhau tuy muc dich, quan trong nhat
        # Fetch result
        records = cursor.fetchall() #luu du lieu cua viec thuc hien cau lenh
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


import random

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import psycopg2
from psycopg2 import Error
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from djangoProject1.common import *
from django.db import models
import random
# Create your models here.
class RegistrationRequest():
    def __init__(self,eid, proposedUserName, proposedPassword, submittedEmailAddress, requestedUserType):
        self.id = eid
        self.proposedUserName = proposedUserName
        self.proposedPassword = proposedPassword
        self.submittedEmailAddress = submittedEmailAddress
        self.requestedUserType = requestedUserType
RegistrationRequests = list()
def MigrateDataRegis():
    data = HookData("DATABASE")
    RegistrationRequests.clear()
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Executing a SQL query
        cursor.execute("select * from registrationrequest")
        # Fetch result
        records = cursor.fetchall()
        # The function code
        for row in records:
            temp = RegistrationRequest(row[0], row[1], row[2], row[3], row[4])
            RegistrationRequests.append(temp)
        for x in RegistrationRequests:
            x.show()
    except (Exception, Error) as error:
        return ("Error while connecting to PostgreSQL")
    finally:
        if (connection):
            cursor.close()
            connection.close()
def SendCredentialMail(email, username, password):
    data = HookData("SENDMAIL")
    fromadd = data["from"]
    toadd = email
    msg = MIMEMultipart()
    msg['From'] = fromadd
    msg['To'] = toadd
    msg['Subject'] = "Credential"
    header = "This is an email automatically sent from BOA Auto Send. Please do not reply to this message!" + "\n"
    footer = "Use the credential to login in BOA"
    body = header + "Username: " + username + "\n" + "Password: " + password + "\n" + footer
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(fromadd, data["password"])
    text = msg.as_string()
    server.sendmail(fromadd, toadd, text)
    server.quit()
    return True
def checkRegisterEmail(request):
    # Read config.ini file
    data = HookData("DATABASE")
    try:
    # Connect to an existing database
        connection = psycopg2.connect(**data)

    # Create a cursor to perform database operations
        cursor1 = connection.cursor()
        cursor2 = connection.cursor()
    # Executing a SQL query
        cursor1.execute("SELECT email_address from boauser;")
        cursor2.execute("SELECT submited_emailadress from registrationrequest;")
    # Fetch result
        record1 = cursor1.fetchall()
        record2 = cursor2.fetchall()
    # The function code
        for row in record1:
            if (request == row[0]):
                return True
        for row in record2:
            if (request == row[0]):
                return True
        return False
    except (Exception, Error) as error:
        return True
    finally:
        if (connection):
            cursor1.close()
            cursor2.close()
            connection.close()
def CreateRegistrationUser(email, usertype):
    if checkRegisterEmail(email) == True:
        return False
    type = re_tranferUsertype(usertype)
    username, password = Create_Credential(email)
    data = HookData("DATABASE")
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        cursor1 = connection.cursor()
        # Executing a SQL query
        cursor1.execute("select count(user_id) from registrationrequest")
        eid = int(cursor1.fetchone()[0]) + 1
        records = ()
        records += (eid, username, password, email, type,)
        query = """insert into registrationrequest(user_id, proposed_username, proposed_password, submited_emailadress, request_user_type) 
                       values (%s,%s,%s,%s,%s)"""
        cursor.execute(query, records)
        connection.commit()
        return True
    except (Exception, Error) as error:
        return False
    finally:
        if (connection):
            cursor.close()
            connection.close()
def DropRequest(email):
    data = HookData("DATABASE")
    drop_data = (email,)
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Executing a SQL query
        query = "delete from registrationrequest where submited_emailadress = %s"
        cursor.execute(query, drop_data)
        connection.commit()
        return True
    except (Exception, Error) as error:
        return ("Error while connecting to PostgreSQL")
    finally:
        if (connection):
            cursor.close()
            connection.close()
def createBOAUser(eid, username, password, email, type):
    data = HookData("DATABASE")
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        print(connection)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        cursor1 = connection.cursor()
        # Executing a SQL query
        records = ()
        records += (eid, username, password, email, type,)
        query = """insert into boauser(eid, user_name, pass_word, email_address, user_type) 
                       values (%s,%s,%s,%s,%s)"""
        cursor.execute(query, records)
        connection.commit()
        return 1
    except (Exception, Error) as error:
        return 0
    finally:
        if (connection):
            cursor.close()
            connection.close()
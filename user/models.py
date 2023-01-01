from django.db import models

# Create your models here.
import psycopg2
from register.models import *
from schedule.models import *
from login.models import *
def UpdateUser(id, newmail, newpassword):
    data = HookData("DATABASE")
    print(data)
    id_fix = int(id)
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        print(connection)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        # Executing a SQL query
        if newmail!='':
            fix = ()
            fix +=(newmail, id_fix, )
            query = """update boauser set email_address=%s where eid=%s"""
            cursor.execute(query, fix)
            connection.commit()
        if newpassword!='':
            fix2 = ()
            fix2 += (newpassword, id_fix, )
            query2 = """update boauser set pass_word=%s where eid=%s"""
            cursor2.execute(query2, fix2)
            connection.commit()
        return 1
    except (Exception, Error) as error:
        return 0
    finally:
        if (connection):
            cursor.close()
            cursor2.close()
            connection.close()
    return 0

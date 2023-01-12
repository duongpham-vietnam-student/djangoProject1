from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import psycopg2
from psycopg2 import Error
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from register.models import *
from djangoProject1.common import *

from schedule.models import MigrateData, Employees
from login.models import MigrateDataBOAUser, BOAUsers
def index(request):
    id = str(request.POST['id'])
    MigrateDataBOAUser()
    for i in BOAUsers:
        if id == str(i.id):
            boa = i
    context = {'id': id, 'boa': boa}
    return render(request, 'register/base.html', context)
def save(request):
            #lay data
            id = str(request.POST['id'])
            email = str(request.POST['email'])
            user_data_type = request.POST['usertype']
            #thuc hien 1 function
            status = CreateRegistrationUser(email, user_data_type)
            context = {'status': status, 'id': id}
            return render(request, 'register/result.html', context)





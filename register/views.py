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
from register.forms import *

def index(request):
    return render(request, 'register/base.html')
def save(request):
    if request.method == "POST":
            email = str(request.POST['email_ros'])
            user_data_type = int(request.POST['usertype'])
            status = CreateRegistrationUser(email, user_data_type)
            context = {'status': status}
    return render(request, 'register/result.html', context)





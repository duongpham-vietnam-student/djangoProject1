from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from login.models import *
import time
# Create your views here.
def index(request):
    return render(request, 'login/login.html')
def login(request):
    if request.method == "POST":
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        print(MigrateDataBOAUser())
        for x in BOAUsers:
            if x.username == username and x.password == password:
                if x.typefix == "ROOT":
                    context = {'user': x, 'id': x.id, 'role': x.typefix, 'request_mode': 1, 'setup_mode': 1, 'edit_mod': 1}
                elif x.typefix == "ADMIN":
                    context = {'user': x, 'id': x.id, 'role': x.typefix, 'setup_mode': 1, 'edit_mode': 1}
                elif x.typefix == "ASSISTANT":
                    context = {'user': x, 'id': x.id, 'role': x.typefix, 'edit_mode': 1}
                elif x.typefix == "EMPLOYEE":
                    context = {'user': x, 'id': x.id, 'role': x.typefix}
                return render(request, 'user/settings.html', context)
        context = {'login':1}
        return render(request, 'login/result.html', context)
def forgot(request):
    username = str(request.POST['username'])
    MigrateDataBOAUser()
    for i in BOAUsers:
        if i.email == username:
            sec = time.time()
            ResetRequestAccount()
            check = RequestAccount("e", username)
            temp, pass_code = Create_Credential(username)
            dataset = (username, sec, pass_code)
            if check==0:
                RequestAccount("i", dataset)
            elif check==1:
                RequestAccount("d", (username,))
                RequestAccount("i", dataset)
            context = {'has_account': 1, }
            return render(request, 'login/result.html', context)
    context = {'no_account':1}
    return render(request, 'login/result.html', context)
def forgot_code(request):
    code = str(request.POST['code'])


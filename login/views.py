from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from login.models import *
import time
# Create your views here.
def index(request):
    return render(request, 'login/login.html') #trang login chua nhap gi vao
def login(request):
    if request.method == "POST":
        submit = str(request.POST['submit'])
        username = str(request.POST['username'])
        password = str(request.POST['password'])
        MigrateDataBOAUser() #lay data tu database
        #database
        #username, password
        if submit == "Login":
            for x in BOAUsers:
                if x.username == username and x.password == password:
                    if x.typefix == "ROOT":
                        context = {'user': x, 'id': x.id, 'role': x.typefix, 'request_mode': 1, 'setup_mode': 1, 'edit_mod': 1}
                        return render(request, 'user/settings.html', context)
                    elif x.typefix == "ADMIN":
                        context = {'user': x, 'id': x.id, 'role': x.typefix, 'setup_mode': 1, 'edit_mode': 1}
                        return render(request, 'user/settings.html', context)
                    elif x.typefix == "ASSISTANT":
                        context = {'user': x, 'id': x.id, 'role': x.typefix, 'edit_mode': 1}
                        return render(request, 'user/settings.html', context)
                    elif x.typefix == "USER":
                        context = {'user': x, 'id': x.id, 'role': x.typefix}
                        return render(request, 'user/settings.html', context)
            context = {'login': 1}
            return render(request, 'login/result.html', context)



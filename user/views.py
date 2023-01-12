from django.shortcuts import render

# Create your views here.
from register.models import *
from user.models import *
from django.http import HttpResponse
# Create your views here.
def setup(request):
    s = str(request.POST['id'])
    MigrateDataBOAUser()
    for x in BOAUsers:
        if str(x.id) == s:
            if x.typefix == "ROOT":
                context = {'user': x, 'id': x.id, 'role': x.typefix, 'request_mode': 1, 'setup_mode': 1, 'edit_mod': 1}
            elif x.typefix == "ADMIN":
                context = {'user': x, 'id': x.id, 'role': x.typefix, 'setup_mode': 1, 'edit_mode': 1}
            elif x.typefix == "ASSISTANT":
                context = {'user': x, 'id': x.id, 'role': x.typefix, 'edit_mode': 1}
            elif x.typefix == "EMPLOYEE":
                context = {'user': x, 'id': x.id, 'role': x.typefix}
    return render(request, 'user/setup.html', context)
def navi(request):
    s = str(request.POST['id'])
    c = str(request.POST['check'])
    if c=="Setup Employee":
        MigrateData()
        context = {'id':s, 'data':Employees}
        return render(request, 'schedule/employee.html', context)
    if c=="Setup Assignment":
        MigrateData()
        context = {'id':s, 'data':Assignments}
        return render(request, 'schedule/assignment.html', context)
    if c=="Setup Shift":
        li, data = shift_config()
        context = {'id':s, 'list':li, 'data':data}
        return render(request, 'schedule/shift.html', context)
def requ(request):
        s = str(request.POST['id'])
        MigrateDataRegis()
        context = {'id': s, 'data': RegistrationRequests}
        return render(request, 'user/requests.html', context)
def sett(request):
        id = str(request.POST['id'])
        MigrateDataBOAUser()
        for x in BOAUsers:
            if str(x.id) == id:
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
def changeinfouser1(request):
    id = str(request.POST['id'])
    context = {'id':id}
    return render(request, 'user/changeinfouser.html', context)
def changeinfouser2(request):
        id = str(request.POST['id'])
        new_mail = str(request.POST['email_ros'])
        new_password = str(request.POST['password'])
        old_password = str(request.POST['password_1'])
        MigrateDataBOAUser()
        for x in BOAUsers:
            if str(x.id) == id:
                idk = id
                if str(x.password) == old_password:
                    s = UpdateUser(id, new_mail, new_password)
                    context = {'status': s, 'id': idk}
                else:
                    s = 0
                    context ={'status': s, 'id': idk}
        return render(request, 'user/changeinfouser_res.html', context)
def accept(request):
        id = str(request.POST['id'])
        context = {'id': id}
        check = str(request.POST['check'])
        submit = str(request.POST['submit'])
        MigrateDataRegis()
        for x in RegistrationRequests:
            MigrateDataBOAUser()
            if str(x.id) == str(check):
                if submit=="Accept":
                    UpdateBOAUser(x.requestedUserType, x.id)
                    DropRequest(x.submittedEmailAddress)
                    context = {'id':id, 'ac':1}
                else:
                    DropRequest(x.submittedEmailAddress)
                    context = {'id':id}
        return render(request, 'user/request_res.html', context)

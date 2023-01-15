from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from schedule.models import *
from register.models import *
from login.models import *
def index(request):
    id = str(request.POST['id'])
    s = list(MigrateSchedule())
    MigrateData()

    for i in s: # sau khi edit nhân vien, nêu chọn xoá nhan vien -> nhan vien bi xoá trong thoi khoá biểu
        find = 0
        for j in Employees:
            if i[0]==j.eid:
                find = 1
        if find==0:
            s.remove(i)

    for i in s: # biến đổi lần lượt id = name cua emp.
        for j in Employees:
            if i[0]==j.eid:
                i[0] = j.name
    for i in range(len(Employees)-len(s)): # edit employee --> thêm nhân viên
        matrix = []
        matrix.append(Employees[len(Employees)+i-1].name)
        for i in range(1,15):
            matrix.append(-1)
        matrix.append(0)
        s.append(matrix)
    context = []
    for i in range(len(Employees)): #upload from employee table to schedule
        temp = []
        context.append(temp)
    for i in range(len(s)): # s la du lieu schedule back-end hieu, context la du lieu schedule hien thi tren web.
        # câu lệnh nay de chuyen s thanh context
        context[i].append(s[i][0]) #them gia trị name cua s vao context
        for j in range(1, 15):
            context[i].append(change(s[i][j]))  #biên đổi thứ tuự chữ số vào asignment tuong ứng
        context[i].append(s[i][15]) # thêm giá trị cost hours



    num, lis= Assignment_fill()  #num=4, lis ["expo", "line", "prep",""] ,expo Am, expo pm--> expo
    list_name_assignment = list(lis)
    super_context = []
    number_week = show_assignment() # số nhân viên làm 1 ca trong tuần
    for i in range(num):
        temp = []
        temp.append(list_name_assignment[i]) # add asignment cua num vào cột đâu tiên cua schedule
        for j in range(len(Shifts)):
            temp.append(number_week[i][j]) # thêm vào số nhân viên cần làm trong tuần theo hang ngang
        super_context.append(temp)
        con = {'schedule': context, 'number_week': super_context, 'id': id} #dictionary
    MigrateDataBOAUser()
    for i in BOAUsers:
        if str(i.id) == id:
            temp = i
    if int(temp.type) > 0: # mode >=1,  phan quyen type > 0, de co quyên edit
        con = {'schedule': context, 'number_week': super_context, 'id': id, 'mode':1}
    return render(request, 'schedule/schedule.html', con)
# Create your views here.


def generate(request):
    id = str(request.POST['id'])
    context = {'id':id}
    submit = str(request.POST['submit'])
    if submit=="Generate Schedule":
        while 1: # tìm cho đến khi tìm dc schedule
            s = create_schedule() #chay thuát toán trong model tim f schedule
            if s == 1:
                return render(request, 'schedule/res.html', context)
    else: #manual edit
        MigrateData()
        num, l = Assignment_fill()
        assi = ["No work"] + list(l) # ("ẽpo",,,"no work")
        context ={'id':id, 'emp':Employees, 'assi':assi}
        return render(request, 'schedule/manual.html', context)

def editempl(request):
        id = str(request.POST['id'])
        submit = str(request.POST['submit'])
        if submit == "Edit Employee":
            check = str(request.POST['check'])
            MigrateData()
            for i in Employees:
                if str(i.eid) == check:
                    context = {'data': i, 'id': id}
                    return render(request, 'schedule/editemploy.html', context)
        elif submit == "Create Employee":
            context = {'id': id}
            return render(request, 'schedule/addemploy.html', context)
        elif submit == "Delete Employee":
            check = str(request.POST['check'])
            dataset = (check,)
            DeleteValue("e", dataset)
            MigrateData()
            context = {'id': id, 'data': Employees}
            return render(request, 'schedule/employee.html', context)
def edit_create_employ(request):
    id = str(request.POST['id'])
    submit = str(request.POST['submit'])
    eid = str(request.POST['eid'])
    name = str(request.POST['name'])
    title = int(request.POST['title'])
    minhour = int(request.POST['minhour'])
    maxhour = int(request.POST['maxhour'])

    if submit == "Accept Create":
        email = str(request.POST['e_mail'])
        dataset = (eid, name, title, minhour, maxhour)
        status = AddValue("e", dataset)
        if status==1:
            username, password = Create_Credential(email)
            SendCredentialMail(email,username,password)
            createBOAUser(eid, username, password, email, "0")
            context = {'create_empl_done':1, 'id':id}
        else:
            context = {'fail': 1, 'id': id}
        return render(request, 'schedule/edit_create_res.html', context)
    elif submit == "Accept Edit":
        old_eid = int(request.POST['old'])
        dataset = (eid, name, title, minhour, maxhour, old_eid)
        status = EditValue("e", dataset)
        if status == 1:
            context = {'edit_empl_done': 1, 'id': id}
        else:
            context = {'fail': 1, 'id': id}
        return render(request, 'schedule/edit_create_res.html', context)
    elif submit == "Navigate Unavailable Time":
        MigrateData()
        context = {'id': id, 'name': name, 'eid': eid}
        for i in Employees:
            if str(i.eid) == eid:
                context = {'id':id, 'data': i.UnavailableTime, 'name':name, 'eid':eid}
                return render(request, 'schedule/unavailabletime.html', context)
        return render(request, 'schedule/unavailabletime.html', context)


def editassi(request):
    id = str(request.POST['id'])
    submit = str(request.POST['submit'])
    if submit == "Edit Assignment":
        check = str(request.POST['check'])
        s = check.split("/")
        MigrateData()
        for i in Assignments:
            if str(i.taskName) == s[0] and i.tag == s[1]:
                context = {'data': i, 'id': id}
                return render(request, 'schedule/editassign.html', context)
    elif submit == "Create Assignment":
        context = {'id': id}
        return render(request, 'schedule/addassign.html', context)
    elif submit == "Delete Assignment":
        check = str(request.POST['check'])
        check_fix = check.split("/")
        dataset = (check_fix[0], check_fix[1])
        DeleteValue("a", dataset)
        UpdateShiftDel(check_fix[0])
        MigrateData()
        context = {'id': id, 'data': Assignments}
        return render(request, 'schedule/assignment.html', context)
def edit_create_assi(request):
    id = str(request.POST['id'])
    submit = str(request.POST['submit'])
    taskname = str(request.POST['taskname'])
    start = str(request.POST['start'])
    end = str(request.POST['end'])
    min_title = int(request.POST['title'])
    tag = str(request.POST['tag'])
    if submit == "Accept Create":
        dataset = (taskname, start, end, min_title, tag)
        status = AddValue("a", dataset)
        if status==1:
            context = {'create_assi_done':1, 'id':id}
            UpdateShift()
        else:
            context = {'fail': 1, 'id': id}
        return render(request, 'schedule/edit_create_res.html', context)
    elif submit == "Accept Edit":
        old = str(request.POST['old'])
        old_s = old.split("/")
        dataset = (taskname, start, end, min_title, tag, old_s[0], old_s[1])
        status = EditValue("a", dataset)
        if status == 1:
            context = {'edit_assi_done': 1, 'id': id}
        else:
            context = {'fail': 1, 'id': id}
        return render(request, 'schedule/edit_create_res.html', context)
class temp_l:
    def __init__(self, l, n ):
        self.l = l
        self.n = n
def editshift(request):
    id = str(request.POST['id'])
    submit = str(request.POST['submit'])
    if submit == "Edit Shift":
        check = str(request.POST['check'])
        s = check.split("/")
        MigrateData()
        for i in Shifts:
            if str(i.day) == s[0] and i.tag == s[1]:
                num, li = Assignment_fill()
                l = list(dict.fromkeys(li))
                num_l = [0]*num
                for j in i.shift_assignment:
                    for k in range(num):
                        if j.assignment.taskName == l[k]:
                            num_l[k] = j.number
                li =[]
                for k in range(num):
                    li.append(temp_l(l[k], num_l[k]))
                context = { 'id': id, 'list':li, 'day':s[0], 'tag':s[1]}
                return render(request, 'schedule/editshift.html', context)
    elif submit == "Delete Shift":
        check = str(request.POST['check'])
        check_fix = check.split("/")
        li, data = shift_config()
        st =""
        for i in range(len(li)):
                st = st + li[i] + "=" + "0" +","
        dataset=(st,)
        dataset+=(check_fix[0], check_fix[1])
        EditValue("s", dataset)
        li, data = shift_config()
        context = {'id': id, 'data': data, 'list':li}
        return render(request, 'schedule/shift.html', context)
def edit_create_shift(request):
    id = str(request.POST['id'])
    n, li = Assignment_fill()
    l = list(dict.fromkeys(li))
    num = [0] * n
    for i in range(n):
        num[i] = int(request.POST[l[i]])

    old = str(request.POST['old'])
    old_s = old.split("/")
    st = ""
    for i in range(n):
        st = st + l[i] + "=" + str(num[i]) + ","
    dataset = (st, old_s[0], old_s[1])
    status = EditValue("s", dataset)
    if status == 1:
        context = {'edit_shift_done': 1, 'id': id}
    else:
        context = {'fail': 1, 'id': id}
    return render(request, 'schedule/edit_create_res.html', context)

def editunav(request):
    id = str(request.POST['id'])
    eid = str(request.POST['eid'])
    name = str(request.POST['name'])
    submit = str(request.POST['submit'])
    if submit == "Edit Unavailable Time":
        check = str(request.POST['check'])
        s = check.split("/")
        MigrateData()
        for i in Employees:
            if str(i.eid) == s[0]:
                for j in i.UnavailableTime:
                    if str(j.day) == s[1] and str(j.start) == s[2]:
                        context = {'data': j, 'id': id, 'eid': eid, 'name': name}
                        return render(request, 'schedule/editunav.html', context)
    elif submit == "Create Unavailable Time":
        context = {'id': id, 'eid': eid, 'name': name}
        return render(request, 'schedule/addunvai.html', context)
    elif submit == "Delete Unavailable Time":
        check = str(request.POST['check'])
        check_fix = check.split("/")
        dataset = (check_fix[0], check_fix[1], check_fix[2])
        DeleteValue("u", dataset)
        MigrateData()
        for i in Employees:
            if str(i.eid) == eid:
                context = {'id':id, 'data': i.UnavailableTime, 'name':name, 'eid':eid}
                return render(request, 'schedule/unavailabletime.html', context)
def edit_create_unav(request):
    id = str(request.POST['id'])
    submit = str(request.POST['submit'])
    eid = str(request.POST['eid'])
    start = str(request.POST['start'])
    end = str(request.POST['end'])
    reason = str(request.POST['reason'])
    day = str(request.POST['day'])
    if submit == "Accept Create":
        dataset = (eid, day, reason, start, end)
        status = AddValue("u", dataset)
        if status==1:
            context = {'create_unav_done':1, 'id':id}
        else:
            context = {'fail': 1, 'id': id}
        return render(request, 'schedule/edit_create_res.html', context)
    elif submit == "Accept Edit":
        old = str(request.POST['old'])
        old_s = old.split("/")
        dataset = (eid, day, reason, start, end, old_s[0], old_s[1], old_s[2])
        status = EditValue("u", dataset)
        if status == 1:
            context = {'edit_unav_done': 1, 'id': id}
        else:
            context = {'fail': 1, 'id': id}
        return render(request, 'schedule/edit_create_res.html', context)
def manual(request):
    id = str(request.POST['id'])
    eid = str(request.POST['emp'])
    day = str(request.POST['day'])
    tag = str(request.POST['tag'])
    assi = str(request.POST['assi'])
    MigrateData()
    num, l = Assignment_fill()
    lis = ["No"] + list(l)
    dataset = [day, tag, assi, lis.index(assi), eid]
    EditValue("sch", dataset)
    context = {'id':id, 'manual':1}
    return render(request, 'schedule/edit_create_res.html', context)


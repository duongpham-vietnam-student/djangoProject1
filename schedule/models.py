from django.db import models
from djangoProject1.common import *
from ortools.sat.python import cp_model
import random
import psycopg2
from psycopg2 import Error
from djangoProject1.common import HookData
UnavailableHours = list()  #list of all UnavailableTimes in database
Employees = list()         #list of all Employee in database
Assignments = list()       #list of all Assignment in database
Shifts = list()         #list of all Shifts in database

# Khai bao cac doi tuong - declare the required objects
class UnavailableHour():     # class này lấy dữ liệu từ bảng Unavailable trong DB - This class gets data from Unavailable table in DB
    def __init__(self, eid, day, reason, start, end):
        self.eid = eid             #id của employee
        self.day = day                  # day of week
        self.reason = reason
        self.start = start          #start time break, for backend calculation
        self.end = end              #end time break
        self.startfix = Time_Tranfer(self.start)      # it's for show data in front end
        self.endfix = Time_Tranfer(self.end)
        # id, day, startime là 3 primary key của bảng này trong DB, nhưng chúng ta cần check thời gian hợp lệ ở back end trước khi thêm vào DB, vì nó không chặt
class Employee():       # class này lấy dữ liệu từ bảng Employee trong DB, và nó lấy cả dữ liệu từ class Unavai phía trên
    def __init__(self, eid , name, title, minhour, maxhour ):
        self.eid = eid    # id của employee
        self.name = name       # name của employee
        self.title = title      #brigate title : 5 rank , number
        self.minhour = minhour      #min work time
        self.maxhour = maxhour      #max work time
        self.UnavailableTime = list()    #các ngày nghỉ của nhân viên, được lấy từ list UnavailableHours
        self.ti = tit_s(self.title)     # brigate title: text for show data in front end
    def setUnTime(self, untime):      #method to add untime
        self.UnavailableTime.append(untime)
class Assignment():         #class này lấy dữ liệu từ bảng asignment trong DB
    def __init__(self, taskName, startTime, endTime, min_title, tag):
        self.taskName = taskName        #name of asignment, it's a primary key
        self.start = startTime  # string, military hour, example 1200 = 12:00 AM
        self.start_fix = Time_Tranfer(startTime)
        self.start_temp = startTime[0:2]+":"+startTime[2:4]
        self.end_fix = Time_Tranfer(endTime)
        self.end = endTime
        self.end_temp = endTime[0:2] + ":" + endTime[2:4]
        self.min_title = min_title  # min title can handle this assigment, value: 1, 2, 3, ...
        self.min_title_fix = tit_s(self.min_title)
        self.tag = tag  # AM or PM
        self.cost = (int(self.end) - int(self.start)) / 100  # chi phí thời gian làm việc,đơn vị hour
class ShiftAssignment():        #class này không có trong DB, nhưng nó được tạo ra để làm cầu nối cho Asignment và Shift
    def __init__(self, numberEmployee, assignment):
        self.number = numberEmployee             #number employee needed for task
        self.assignment = assignment                      #Class Assignment

class Shift():                  #class này lấy dữ liệu từ bảng Shift trong DB
    def __init__(self, day, tag):
        self.day = day  # day of week: Mon, Tue, Wed,...
        self.tag = tag  # AM or PM
        self.shift_assignment = list()  # list of ShiftAssignment
        self.rank = shift_rank(self.day, self.tag)
    def setShift(self, tag, text):  # a method to add ShiftAssignment to Shift
        text1 = text.split(',')  #trong DB, được mô tả dưới dạng 1 chuỗi text, có dạng Line=3,Dishwasher=0,...
        texts = list()
        for temp in text1:    #text1 = [["Line=3"], ["Dishwasher=0"],...]]
            text2 = temp.split('=')
            texts.append(text2)
        for y in texts:
            for x in Assignments:
                if x.taskName == y[0] and x.tag==tag:
                    sa = ShiftAssignment(int(y[1]), x)
                    self.shift_assignment.append(sa)

    #check two function
    def minShift(self):
        min = 5
        for x in self.shift_assignment:
            if min > int(x.assignment.min_title):
                min = int(x.assignment.min_title)
        return min
    def maxShift(self):
        max = 0
        for x in self.shift_assignment:
            if max < int(x.assignment.min_title):
                max = int(x.assignment.min_title)
        return max
    #...
def shift_assignment_config(a):
    li = []
    for i in a.shift_assignment:
        li.append(i.assignment.taskName)
    return li
def shift_config():
    MigrateData()
    num, lis = Assignment_fill()
    lis_fix = list(dict.fromkeys(lis))

    li = sorted(Shifts, key = take_point)
    data = []
    for i in li:
        lis_com = shift_assignment_config(i)
        temp = []
        temp.append(i.day)
        temp.append(i.tag)
        for j in range(num):
            if lis_fix[j] not in lis_com:
                temp.append(0)
            for k in i.shift_assignment:
                if lis_fix[j]==k.assignment.taskName:
                     temp.append(k.number)
        data.append(temp)

    return lis_fix, data

def convertData():              #function này tạo ra ma trận những ngày có thể làm việc của các nhân viên
    res = list()
    for e in Employees:
        temp = [int(e.title)] * len(Shifts)      #tạm thời cho tất cả đều có khả năng work mọi ca
        res.append(temp)
    i = 0
    j = 0
    for e in Employees:
        for s in Shifts:
            min = s.minShift()
            if len(s.shift_assignment)==0 or min>int(e.title):   #không có ngày làm việc, hoặc yêu cầu tối thiểu ngày đó lớn hơn khả năng nhân viên
                res[i][j] = -1    # không thể work
            # code check xem nhân viên đó có bận không? 4 dòng
            for a in Assignments:
                for u in e.UnavailableTime:
                    if s.day==u.day and a.start>=u.start and a.end<=u.end:
                        res[i][j] = -1   # không thể work
            j+=1    #j đại diện cho ca làm, +1 cuối lệnh for của shift
        j=0         #reset lại với employ khác
        i+=1        #+1 cho mỗi employee
    return res
def returnESR(a):       #này để chỉnh dữ liệu thôi
        return str(a).split("-")
def CheckE2(y, li):
    y2 = returnESR(y)
    for x in li:
        if y2[0] == x[0] and y2[2] != x[2]:
            return 1
    return 0
def divide_Assignments():
    Assignments_AM = list()
    Assignments_PM = list()
    for i in Assignments:
        if i.tag=="AM":
            Assignments_AM.append(i)
        else:
            Assignments_PM.append(i)
    return Assignments_AM, Assignments_PM
def poss_day(s, all): #Step 3
    am, pm = divide_Assignments()
    if Shifts[int(s)].tag == "AM":
        req = [0] * len(am)
        req_com = [0] * len(am)
    else:
        req = [0] * len(pm)
        req_com = [0] * len(pm)
    li = []
    poss_list = []
    choi = []
    for x in all:
        if int(returnESR(x)[1]) == s:
            poss_list.append(x)
    h = convertData()
    for x in poss_list:
        a = returnESR(x)
        i = int(a[0])
        j = int(a[1])
        k = int(a[2])
        if h[i][j] == -1 or int(Employees[i].title) < int(Shifts[j].shift_assignment[k].assignment.min_title):
            poss_list.remove(x)

    temp1 = Shifts[int(s)].shift_assignment
    for x in temp1:
        req[temp1.index(x)] = int(x.number)
    for i in range(len(poss_list)):
        choi.append(i)
    while len(choi)>1:
        val = random.choice(choi)
        choi.remove(val)
        z = int(returnESR(poss_list[val])[2])
        if CheckE2(poss_list[val], li) == 0 and req[z] > 0:
            li.append(returnESR(poss_list[val]))
        req[z] = req[z] - 1
        if req == req_com:
            break
    return li
def em_cost(a):
    s = int(a[1])
    num, li = Assignment_fill()
    lis = list(li)
    r = int(a[2])
    for i in Assignments:
        if i.taskName == lis[r] and i.tag == Shifts[s].tag:
            return i.cost
def check_critia(a):
    cost = push_critia(a)
    penalty = 0
    sum = 0
    for i in range(len(Employees)):
        if Employees[i].minhour > cost[i] or Employees[i].maxhour < cost[i]:
            sum += 1
            penalty += 1
            if Employees[i].minhour > cost[i] + 3 or Employees[i].maxhour < cost[i] - 3:
                penalty += 3
            if Employees[i].minhour > cost[i] + 6 or Employees[i].maxhour < cost[i] - 6:
                penalty += 7
    if (penalty < 10 and sum < 3):

        return 1
    else:
        return 0
def push_critia(a):    #số giờ làm việc của mỗi nhân viên trong schedule
    cost = [0] * len(Employees)
    for i in a:
        cost[int(i[0])] = cost[int(i[0])] + em_cost(i)
    return cost
def Assignment_fill():
    li = []
    for i in Assignments:
        li.append(i.taskName)
    li = dict.fromkeys(li)
    return len(li), li
def schedule():
    model = cp_model.CpModel()
    shift = {}
    all_list = []
    poss_list = []
    week_list = []
    role, li = Assignment_fill()
    for e in range(len(Employees)):
        for s in range(len(Shifts)):
            for r in range(role):
                shift[(e, s, r)] = model.NewBoolVar('%i-%i-%i' % (e, s, r))
                all_list.append(shift[(e, s, r)])
    stop = 0
    while (stop == 0):
        for s in range(len(Shifts)):
            poss_list.append(poss_day(s, all_list))
        for i in range(len(poss_list)):
            week_list = week_list + poss_list[i]
        if check_critia(week_list) == 1:
            stop = 1
        else:
            week_list = []
            poss_list = []
    return week_list, push_critia(week_list)
def MigrateData():
    data = HookData("DATABASE")
    Employees.clear()
    Shifts.clear()
    UnavailableHours.clear()
    Assignments.clear()
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor_e = connection.cursor()
        cursor_u = connection.cursor()
        cursor_a = connection.cursor()
        cursor_s = connection.cursor()
        # Executing a SQL query
        cursor_e.execute("select * from employee")
        cursor_u.execute("select * from unavailabletime")
        cursor_a.execute("select * from assignments")
        cursor_s.execute("select * from shifts")
        # Fetch result
        record_e = cursor_e.fetchall()
        record_u = cursor_u.fetchall()
        record_a = cursor_a.fetchall()
        record_s = cursor_s.fetchall()
        # The function code
        for row in record_e:
            temp = Employee(row[0], row[1], row[2], row[3], row[4])
            Employees.append(temp)
        for row in record_u:
            temp = UnavailableHour(row[0], row[1], row[2], row[3], row[4])
            UnavailableHours.append(temp)
        for x in UnavailableHours:
            for y in Employees:
                if x.eid == y.eid:
                    y.setUnTime(x)
        for row in record_a:
            temp = Assignment(row[0], row[1], row[2], row[3], row[4])
            Assignments.append(temp)
        for row in record_s:
            temp = Shift(row[0], row[1])
            temp.setShift(row[1], row[2])
            Shifts.append(temp)
    except (Exception, Error) as error:
        return ("Error while connecting to PostgreSQL")
    finally:
        if (connection):
            cursor_e.close()
            cursor_u.close()
            cursor_a.close()
            cursor_s.close()
            connection.close()
def findShift(day, tag):
    for i in range(len(Shifts)):
        if Shifts[i].day == day and Shifts[i].tag == tag:
            return i
def create_schedule():
    MigrateData()
    a, b = schedule()
    e = []
    for j in range(len(Employees)):
        temp = [-1]*14
        e.append(temp)
    for i in range(len(Employees)):
        for j in range(14):
            for k in a:
                u1, u2= re_day_range(j)
                u3 = findShift(u1, u2)
                if i == int(k[0]) and u3==int(k[1]):
                    e[i][j] = int(k[2])
    data = HookData("DATABASE")
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Executing a SQL query

        cursor.execute("delete from schedule")
        for i in range(len(Employees)):
            records = ()
            records += (Employees[i].eid,)
            for j in range(14):
                records += (e[i][j],)
            records += (b[i],)
            query = """insert into schedule(eid, monam, monpm, tueam, tuepm, wedam, wedpm, thuam, thupm, friam, fripm, satam, satpm, sunam, sunpm, c_hour) 
                       values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

            cursor.execute(query, records)
            connection.commit()
        return 1
    except (Exception, Error) as error:
        return 0
    finally:
        if (connection):
            cursor.close()
            connection.close()
    return 1
def MigrateSchedule():
    MigrateData()
    data = HookData("DATABASE")
    try:
        # Connect to an existing database
        connection = psycopg2.connect(**data)
        # Create a cursor to perform database operations
        cursor_e = connection.cursor()
        # Executing a SQL query
        cursor_e.execute("select * from schedule")
        # Fetch result
        record_e = cursor_e.fetchall()
        # The function code
        return record_e
    except (Exception, Error) as error:
        return 0
    finally:
        if (connection):
            cursor_e.close()
def AddValue(command, dataset):
    data = HookData("DATABASE")
    if command=="e":
        try:
            print("e")
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            print(connection)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            query = """insert into employee(eid, e_name, e_title, e_minhour, e_maxhour) 
                               values (%s,%s,%s,%s,%s)"""
            cursor.execute(query, dataset)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
    elif command=="u":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            print(connection)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            query = """insert into unavailabletime(eid, day_of_week, reason, time_start, time_end) 
                               values (%s,%s,%s,%s,%s)"""
            cursor.execute(query, dataset)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
    elif command=="a":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)

            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            query = """insert into assignments(task_name, start_time, end_time, min_title, tag) 
                               values (%s,%s,%s,%s,%s)"""
            cursor.execute(query, dataset)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
def choose_Query_Schedule(day, tag):
    if day=='Mon' and tag=='AM':
        return "update schedule set monam=%s where eid=%s"
    if day=='Mon' and tag=='PM':
        return "update schedule set monpm=%s where eid=%s"
    if day=='Tue' and tag=='AM':
        return "update schedule set tueam=%s where eid=%s"
    if day=='Tue' and tag=='PM':
        return "update schedule set tuepm=%s where eid=%s"
    if day=='Wed' and tag=='AM':
        return "update schedule set wedam=%s where eid=%s"
    if day=='Wed' and tag=='PM':
        return "update schedule set wedpm=%s where eid=%s"
    if day=='Thu' and tag=='AM':
        return "update schedule set thuam=%s where eid=%s"
    if day=='Thu' and tag=='PM':
        return "update schedule set thupm=%s where eid=%s"
    if day=='Fri' and tag=='AM':
        return "update schedule set friam=%s where eid=%s"
    if day=='Fri' and tag=='AM':
        return "update schedule set fripm=%s where eid=%s"
    if day=='Sat' and tag=='AM':
        return "update schedule set satam=%s where eid=%s"
    if day=='Sat' and tag=='AM':
        return "update schedule set satpm=%s where eid=%s"
    if day=='Sun' and tag=='AM':
        return "update schedule set sunam=%s where eid=%s"
    if day=='Sun' and tag=='PM':
        return "update schedule set sunpm=%s where eid=%s"
def EditValue(command, dataset):
    data = HookData("DATABASE")

    if command=="e":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            dataset_fix = tuple(dataset)
            query = """update employee set eid=%s, e_name=%s, e_title=%s, e_minhour=%s, e_maxhour=%s where eid=%s"""
            cursor.execute(query, dataset_fix)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
    elif command=="u":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            query = """update unavailabletime set eid=%s, day_of_week=%s, reason=%s, time_start=%s, time_end=%s where eid=%s"""
            dataset_fix = tuple(dataset)
            cursor.execute(query, dataset_fix)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
    elif command=="a":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            query = """update assignments set task_name=%s, start_time=%s, end_time=%s, min_title=%s, tag=%s where task_name=%s and tag=%s"""
            dataset_fix = tuple(dataset)
            cursor.execute(query, dataset_fix)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
    elif command=="s":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            query = """update shifts set description=%s where day_of_week=%s and tag=%s"""
            dataset_fix = tuple(dataset)
            cursor.execute(query, dataset_fix)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
    elif command=="sch":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            query = choose_Query_Schedule(dataset[0], dataset[1])
            dataset_fix = tuple(dataset[2:])
            cursor.execute(query, dataset_fix)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
def DeleteValue(command, dataset):
    data = HookData("DATABASE")
    if command=="e":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            cursor.execute("delete from employee where eid=%s", dataset)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
    elif command=="u":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            cursor.execute("delete from unavailable where eid=%s", dataset)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
    elif command=="a":
        try:
            # Connect to an existing database
            connection = psycopg2.connect(**data)
            # Create a cursor to perform database operations
            cursor = connection.cursor()
            # Executing a SQL query
            cursor.execute("delete from assignments where task_name=%s and tag=%s", dataset)
            connection.commit()
            return 1
        except (Exception, Error) as error:
            return 0
        finally:
            if (connection):
                cursor.close()
                connection.close()
        return 0
def take_point(a):
    return a.rank
def change(s):
    if s == 0 :
        return "Dishwasher"
    elif s==1:
        return "Line"
    elif s==2:
        return "Prep"
    elif s==3:
        return "Expo"
    elif s==-1:
        return "No work"
def show_assignment():
    MigrateData()
    li = sorted(Shifts, key= take_point)
    num, lis = Assignment_fill()
    list_name_assignment = list(lis)
    number_week = []
    number_day = [0] * len(li)
    for k in range(num):
        for i in li:
            for j in i.shift_assignment:

                if j.assignment.taskName == list_name_assignment[k]:
                    number_day[li.index(i)] = j.number

        number_week.append(number_day)
        number_day = [0] * len(li)
    return number_week














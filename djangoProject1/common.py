from configparser import ConfigParser
from pathlib import Path
import string
import random
def HookData(request):
    config = ConfigParser()

    basepath = Path(__file__).parent      #djangopj1/common.py ->djangopj1
    filepath = (basepath/"config.ini").resolve()  #->djangopj1/config.py
    # "C://..../config.ini"

    config.read(filepath)

    return dict(config.items(request))
def tranferUsertype(request):
    if int(request) >= 3:
        return "ROOT"
    elif int(request) == 2:
        return "ADMIN"
    elif int(request) == 1:
        return "ASSISTANT"
    elif int(request) == 0:
        return "USER"
def re_tranferUsertype(request):
    if request.upper() == "ROOT":
        return 3
    elif request.upper() == "ADMIN":
        return 2
    elif request.upper() == "ASSISTANT":
        return 1
    else:
        return 0
def Create_Credential(email):
    username = email.split('@')[0]
    character = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(character) for i in range(8))
    return username, password
def Time_Tranfer(s):
    if s <= "1200":
        res = s[0:2] + ":" + s[2:4]+ "AM"
        return res
    else:
        hour = (int(s[0:2]) - 12)
        if hour<10:
            hour = '0' + str(hour)
        else:
            hour = str(hour)
        res = hour + ":" + s[2:4] + "PM"
        return res

def reTime_Transfer(s, tag):
    if tag=="AM":
        return s
    else:
        fix = (int(s) + 12)
        return str(fix)
def tit_s(self):
    if self == "4":
        return "Kitchen Leader"
    elif self == "3":
        return "Sous chief"
    elif self == "2":
        return "Line cook"
    elif self == "1":
        return "Junior cook"
    elif self == "0":
        return "Dishwasher"
def shift_rank(day, tag):
    #gan 1 con so dai dien cho ca lam viec, dung de sap xep theo thu tu thoi gian
    if day == "Mon" and tag == "AM":
         return 0
    if day == "Mon" and tag == "PM":
        return 1
    if day == "Tue" and tag == "AM":
        return 2
    if day == "Tue" and tag == "PM":
        return 3
    if day == "Wed" and tag == "AM":
        return 4
    if day == "Wed" and tag == "PM":
        return 5
    if day == "Thu" and tag == "AM":
        return 6
    if day == "Thu" and tag == "PM":
        return 7
    if day == "Fri" and tag == "AM":
        return 8
    if day == "Fri" and tag == "PM":
        return 9
    if day == "Sat" and tag == "AM":
        return 10
    if day == "Sat" and tag == "PM":
        return 11
    if day == "Sun" and tag == "AM":
        return 12
    if day == "Sun" and tag == "PM":
        return 13

def re_day_range(num):
    #tu trong so tim ra ca lam viec: 5
    if num // 2 == 0:
        day = "Mon"
    elif num // 2 == 1:
        day = "Tue"
    elif num // 2 == 2:
        day = "Wed"
    elif num // 2 == 3:
        day = "Thu"
    elif num // 2 == 4:
        day = "Fri"
    elif num // 2 == 5:
        day = "Sat"
    elif num // 2 == 6:
        day = "Sun"
    if num % 2 == 0:
        tag = "AM"
    elif num % 2 == 1:
        tag = "PM"
    return day, tag



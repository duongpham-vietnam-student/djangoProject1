
from configparser import ConfigParser
#Get the configparser object
config_object = ConfigParser()

config_object["DATABASE"] = {
                                  "user": "admin1",
                                  "password": "1234567",
                                  "host": "4.tcp.ngrok.io", #local
                                  "port": "17339",
                                  "database": "BOAProject"
                                }
config_object["SENDMAIL"] = {
                                  "From": "autosend67@gmail.com",
                                  "Password": "gddrwplnkllnxepn",
                                }


#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
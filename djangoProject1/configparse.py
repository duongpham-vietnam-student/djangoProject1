
from configparser import ConfigParser
#Get the configparser object
config_object = ConfigParser()

config_object["DATABASE"] = {
                                  "user": "admin1",
                                  "password": "1234567",
                                  "host": "127.0.0.1", #local
                                  "port": "5433",
                                  "database": "BOAProject"
                                }
config_object["SENDMAIL"] = {
                                  "From": "autosend67@gmail.com",
                                  "Password": "gddrwplnkllnxepn", #password ung dung
                                }


#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
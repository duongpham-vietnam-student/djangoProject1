
from configparser import ConfigParser
#Get the configparser object
config_object = ConfigParser()

config_object["DATABASE"] = {
                                  "user": "postgres",
                                  "password": "12345678",
                                  "host": "database-2.c7u3agesyras.us-east-1.rds.amazonaws.com",
                                  "port": "5433",
                                  "database": "BOAProject"
                                }
config_object["SENDMAIL"] = {
                                  "From": "autosend67@gmail.com",
                                  "Password": "gddrwplnkllnxepn",
                                }


#Write the above sections to config.ini file
with open('config.ini', 'w') as conf:
    config_object.write(conf)
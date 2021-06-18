# stores all the configuartion done to the app
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    
    SQLALCHEMY_DATABASE_URI        = 'sqlite:///' + os.path.join(basedir+'\\data\\data','data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER                  = basedir + '\\data\\files'
    ALLOWED_EXTENSIONS             = set(['csv', 'txt'])    
    SECRET_KEY                     = 'secret'

import os

class BaseSettings(object):
    DEBUG = True
    DEFAULT_FROM_EMAIL = "noreply@lbc-property-sorter.herokuapp.com"
    EMAIL_SUBJECT_PREFIX = "[LBC Property Sorter] "

class ProductionSettings(BaseSettings):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ADMINS = [os.environ.get('ADMIN_EMAIL')]
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('SENDGRID_USERNAME')
    MAIL_PASSWORD = os.environ.get('SENDGRID_PASSWORD')

class DevelopmentSettings(BaseSettings):
    DEBUG = True
    # python2 -c "import os; print os.urandom(24).encode('base64')"
    SECRET_KEY = "E5yy76IDJ4bSQHesuPmMAPJEH6/dovkU"

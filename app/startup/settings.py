import os


# *****************************
# Environment specific settings
# *****************************

APP_NAME = "SimpleMetrics"

# The settings below can (and should) be over-ruled by OS environment variable settings

# Flask settings                     # Generated with: import os; os.urandom(24)
SECRET_KEY = os.environ.get('SECRET_KEY')
# PLEASE USE A DIFFERENT KEY FOR PRODUCTION ENVIRONMENTS!
                                                    
# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Cache settings


# Flask-Mail settings
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME')
MAIL_SERVER = 'mail.getsimplemetrics.com'
MAIL_PORT = 587
MAIL_USE_SSL = 0  # Use '1' for True and '0' for False
MAIL_USE_TLS = 1  # Use '1' for True and '0' for False

ADMINS = []
admin1 = os.getenv('ADMIN1', '"Admin One" <admin1@gmail.com>')
admin2 = os.getenv('ADMIN2', '')
admin3 = os.getenv('ADMIN3', '')
admin4 = os.getenv('ADMIN4', '')
if admin1: ADMINS.append(admin1)
if admin2: ADMINS.append(admin2)
if admin3: ADMINS.append(admin3)
if admin4: ADMINS.append(admin4)


# ***********************************
# Settings common to all environments
# ***********************************

# Application settings
APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

# Flask settings
CSRF_ENABLED = True

# Flask-User settings
USER_APP_NAME = APP_NAME
USER_AFTER_LOGIN_ENDPOINT = 'index'
USER_AFTER_LOGOUT_ENDPOINT = 'welcome'
USER_AFTER_CONFIRM_ENDPOINT = 'plans'
USER_AFTER_REGISTER_ENDPOINT = 'getstarted'
USER_AFTER_RESET_PASSWORD_ENDPOINT = 'user_profile_page'
USER_AFTER_CHANGE_USERNAME_ENDPOINT = 'user_profile_page'

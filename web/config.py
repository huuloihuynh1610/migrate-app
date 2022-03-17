import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="migrate-project-pgserver-jpwest.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="azureuser@migrate-project-pgserver-jpwest" #TODO: Update value
    POSTGRES_PW="Huuloi1995"   #TODO: Update value
    POSTGRES_DB="migrateprojectdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'JyhxuasJm843AWTID7BXZbdHfAryjepvATh2e6XRmC4='
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://migrate-project-servicebus-jpwest.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=JyhxuasJm843AWTID7BXZbdHfAryjepvATh2e6XRmC4=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'phieu.boy1995@gmail.com'
    SENDGRID_API_KEY = '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' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
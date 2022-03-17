import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(float(msg.get_body().decode('utf-8')))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
    conn = psycopg2.connect(dbname="migrateprojectdb",
                            user="azureuser@migrate-project-pgserver-jpwest",
                            password="Huuloi1995",
                            host="migrate-project-pgserver-jpwest.postgres.database.azure.com")
    curs = conn.cursor()
    try:
        # TODO: Get notification message and subject from database using the notification_id
        curs.execute("SELECT subject, message FROM notification WHERE id={};".format(notification_id))
        result = curs.fetchall()
        subject, body = result[0][0], result[0][1]
        # TODO: Get attendees email and name
        curs.execute("SELECT email, first_name FROM attendee;")
        attendees = curs.fetchall()
        # TODO: Loop through each attendee and send an email with a personalized subject
        for (email, first_name) in attendees:
            mail = Mail(
                from_email="phieu.boy1995@gmail.com",
                to_emails= email,
                subject= subject,
                plain_text_content="Hello {}, \n {}".format(first_name, body))
            try:
                SEND_GRID_API_KEY = "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"
                sg = SendGridAPIClient(SEND_GRID_API_KEY)
                response = sg.send(mail)
            except Exception as e:
                logging.error(e)
        status = "Notified {} attendees".format(len(attendees))
        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        curs.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(status, datetime.utcnow(), notification_id))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        conn.rollback()
    finally:
        # TODO: Close connection
        curs.close()
        conn.close()

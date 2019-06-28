import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path


class Watcher:
    DIRECTORY_TO_WATCH = "/home/arts/powershell_ftp"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received FTP Import: - %s." % event.src_path)
            log_location = event.src_path
            subject_name = log_location[26:36]
            print("FTP Received for Track: ", subject_name)
            email = 'kris.stobbe@sas.com' # Your email
            send_to_email = 'support@sas.com' # Who you are sending the message to
            subject = subject_name # The subject line
            message = 'This is a test Email from the SAS Log Collector Python Email Server' # The message in the email
            file_location = log_location

            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = send_to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(message, 'plain'))

            # Setup the attachment
            filename = os.path.basename(file_location)
            attachment = open(file_location, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

            # Attach the attachment to the MIMEMultipart object
            msg.attach(part)
            server = smtplib.SMTP('mailhost.fyi.sas.com', 25) # Connect to the server
            server.starttls() # Use TLS
            server.set_debuglevel(1)
            text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
            server.sendmail(email, send_to_email, text)
            server.quit()

            # SENDS LOG VIA FTP to Track
            from ftplib import FTP
            ftp = FTP('ftp.sas.com')
            ftp.login()  
            ftp.cwd('/techsup/upload')

            def placeFile():
                filename = subject_name+'.txt'
                ftp.storbinary('STOR '+filename, open(filename, 'rb'))
                ftp.quit()
                
            placeFile()


if __name__ == '__main__':
    w = Watcher()
    w.run()
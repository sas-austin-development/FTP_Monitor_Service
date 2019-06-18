import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import smtplib


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
            # email = 'saslogcollector@gmail.com' # Your email
            # password = 'test01**test' # Your email account password
            # send_to_email = 'krisstobbe@yahoo.com' # Who you are sending the message to
            # message = 'This is my message' # The message in the email

            # server = smtplib.SMTP('mailhost.fyi.sas.com', 25) # Connect to the server
            # server.starttls() # Use TLS
            # server.login(email, password) # Login to the email server
            # server.sendmail(email, send_to_email , message) # Send the email
            # server.quit() # Logout of the email server


if __name__ == '__main__':
    w = Watcher()
    w.run()
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
            folder_name = event.src_path
            subject_name = folder_name[26:36]
            print(subject_name)


if __name__ == '__main__':
    w = Watcher()
    w.run()
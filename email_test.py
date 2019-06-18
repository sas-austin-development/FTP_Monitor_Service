import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path

email = 'saslogcollector@sas.com' # Your email
password = 'password' # Your email account password
send_to_email = 'kris.stobbe@sas.com' # Who you are sending the message to
subject = 'This is the subject' # The subject line
message = 'Python Test Email' # The message in the email
file_location = '/home/arts/Downloads/step6v2.jpg'

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
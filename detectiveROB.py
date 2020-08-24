import sys
import pygtail
from pygtail import Pygtail
import subprocess
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

getContact = '/opt/customlogger/mycontacts.txt'     # This path need to update as per directory
TemplateMessage = '/opt/customlogger/message.txt'   # This path need to update as per directory

MY_ADDRESS = 'info@airfinder.com'               # This line need to update as per requirement
SESUser = 'XXXXXXXX'
PASSWORD = 'XXXXXXXX'                            # This line need to update as per requirement
SmtpHost = 'email-smtp.us-east-1.amazonaws.com'                     # This line need to update as per requirement
SmptpPort = '587'                               # This line need to update as per requirement

def get_contacts(getContact):
    names = []
    emails = []
    with open(getContact, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(TemplateMessage):
    with open(TemplateMessage, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def mailerFunction():
    names, emails = get_contacts(getContact) # read contacts
    message_template = read_template(TemplateMessage)
 # set up the SMTP server
    s = smtplib.SMTP(host= SmtpHost, port=SmptpPort)
    s.starttls()
    s.login(SESUser, PASSWORD)
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']= MY_ADDRESS
        msg['To']= email
        msg['Subject']="This is TEST"
        
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        
        # send the message via the server set up earlier.
        s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

# This function is used to restart nginx service
def restartNginx():
    print("Restarting Nginx....")
    subprocess.call(['supervisorctl', 'start', 'cloud-canary'])
    subprocess.call(['supervisorctl', 'start', 'cloud-canary'])

## Define your pattern here for log catch
pattern = 'Too many open files'                       # Log Pattern to match from logs   
restartValue = '0'                    # Global value to check service need to restart or not  
LogFile = "/var/log/supervisor/cloud-canary-stdout---supervisor-xroSdT.log" # Log file full path
NormalMessage = "No error found"
# This function is tailing log file and checking agains pattern 
def tailer ():
    for line in Pygtail(LogFile):
        if pattern in line:
            global restartValue
            restartValue = "1"

# This variable checking value to restart nginx 
def checkVal ():
    if restartValue == '1':
        restartNginx()
        mailerFunction()
    else:
        print(NormalMessage)

# Calling required functions 
tailer()
checkVal()

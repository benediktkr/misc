 # rsnapshot settings
rsnap_bin = "/usr/bin/rsnapshot"
interval = "daily" 

 # Email settings
mailfrom = "root"
mailto = "benedikt"
mailsubject = "Backup error"
mailifgood = False             # Send email if everything went fine?

#####################

from subprocess import Popen, PIPE
from socket import gethostname
import smtplib
from email.mime.text import MIMEText

rsnap = Popen([rsnap_bin, interval], stdout=PIPE, stderr=PIPE, stdin=PIPE)
rsnap_comm = rsnap.communicate()

if (rsnap.returncode != 0):
    # print out stderr
    # 0 = stdout, 1 = stderr
    print rsnap_comm[1]
    
    # MIME enc the stderr
    msg = MIMEText("stderr \n " + rsnap_comm[1])
    msg['Subject'] = mailsubject + ": " + gethostname()
    msg['From'] = "Rsnapshot Backup <" + mailfrom + ">"
    msg['To'] = mailto
    
    s = smtplib.SMTP()
    s.connect()
    s.sendmail(mailfrom, mailto, msg.as_string())

elif (mailifgood):
    # print stdout
    print rsnap_comm[0]
    msg = MIMEText("stdout \n " + rsnap_comm[0])
    msg['Subject'] = "Sucessfull backup: " + gethostname()
    msg['From'] = "Rsnapshot Backup <" + mailfrom + ">"
    msg['To'] = mailto
    
    s = smtplib.SMTP()
    s.connect()
    s.sendmail(mailfrom, mailto, msg.as_string())

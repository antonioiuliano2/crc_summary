import os
import smtplib
import elog
import sys
#connect to your electronic logbook
elog_crc = elog.open("http://yourelogserver.org","CRCs",user="username",password="password",port=8080,use_ssl=False)

deltaT = 1800 #time between ELOG checks in seconds

#SMTP configuration

SMTPport = 500 #replace with SMTPport of your domain

mailserver = smtplib.SMTP("domain.org",SMTPport)
# identify ourselves to smtp client
mailserver.ehlo()
# secure our email with tls encryption
mailserver.starttls()
# re-identify ourselves as an encrypted connection
mailserver.ehlo()
mailserver.login('mailusername', 'mailpassword')

def readCRClogs(CRC_log):
    '''reading log from CRC, checking which telescopes are transmitting
       example of line for the coding
    #'    <telescope latitudine="42" longitudine="0" port="7705" status="Waiting" ReceiverPWD="" SenderPWD="">Surface</telescope>\n'
       '''
    status_telescopes = {}
    with open(CRC_log,'r') as CRC_file:
        for line in CRC_file:
            if "telescope" in line:
                #split the line, retrieve the status and the port
         
                line_array = line.split()        
                status = line_array[4][8:-1]
                  
                port = line_array[3][6:-1]         
        
                status_telescopes[int(port)] = status

    return status_telescopes

def notify_email(Referente, Email_Referente, Posizione, mailserver, downtime):
    '''CRC is not working, please have a look a it'''
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    
    print("CRC from ",Posizione," is not online. with downtime ", downtime)
    print("Notification sent to ", Referente)
    print("at email ", Email_Referente,"?")
    print("\n")
    
    recipients = [Email_Referente,'username@myprovider.org'] #sending it also to myself for copy
    #preparing message
    msg = MIMEMultipart()
    msg['From'] = 'crcalert@network.org'
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = 'CRCNetwork warning message'
    message = 'CRC from {} has not been online for one day. Please check'.format(Posizione)
    msg.attach(MIMEText(message))

    mailserver.sendmail('crcalert@network.org',recipients,msg.as_string())


status_telescopes = readCRClogs(sys.argv[1])

for ientry in elog_crc.get_message_ids():
    message, attributes, attachments = elog_crc.read(ientry)
    CRCport = int(attributes["Porta Seriale"])
    
    ELOG_status = bool(int(attributes["In rete"])) #is it currently reported as online or offline?
    Monitoring_flag = bool(int(attributes["Monitora se in rete"]))
    if (Monitoring_flag):
        downtime = float(attributes["Ore non in rete"]) #get current value
        CRC_status = status_telescopes[CRCport]
        
        if CRC_status == "Transmitting" and not ELOG_status: #ELOG entry was offline, updating it to online
            elog_crc.post('',ientry, attributes={"In rete":1, "Ore non in rete":0})
        
        if CRC_status == "Waiting":
            if downtime == 24: #for now, only send the email the first time it is found offline, then we can set a threshold
             notify_email(attributes["Referente"], attributes["Email Referente"], attributes["Posizione di Assegnazione"], mailserver, downtime)
            downtime = downtime + (deltaT/3600.) #increase it by deltaT (downtime is in hour, deltaT is in seconds)
            if ELOG_status: #ELOG entry was online, updating it to offline
               elog_crc.post('',ientry, attributes={"In rete":0, "Ore non in rete":round(downtime,1)})
            else:
                elog_crc.post('',ientry,attributes={"Ore non in rete":round(downtime,1)})

mailserver.quit()

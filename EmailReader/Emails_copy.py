
from email.message import EmailMessage
import ssl
import smtplib

import imaplib
import email

class EmmaMail:
    password=""
    emailFrom=""
    
    def Read(self):#self
        print("Running")
        email_command=['none','none']
        #credentials
        # https://www.systoolsgroup.com/imap/
        gmail_host= 'imap.gmail.com'
        try:
            #set connection
            mail = imaplib.IMAP4_SSL(gmail_host)
        except:
            return "no_connection"
        #login
        mail.login(self.emailFrom, self.password)
        #select inbox
        mail.select("INBOX")
        #select specific mails
        _, selected_mails = mail.search(None, 'UNSEEN')
        #total number of mails from specific user
        for num in selected_mails[0].split():
            _, data = mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]
        
            #convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)
        
            #access data
            SUBJECT=["Subject: ",email_message["subject"].lower()]
            TO=["To:", email_message["to"].lower()]
            FROM=["From: ",email_message["from"].lower()]
            DATE=["Date: ",email_message["date"]]
        
            for part in email_message.walk():
                if part.get_content_type()=="text/plain" or part.get_content_type()=="text/html":
                    print("Text")
                    message = part.get_payload(decode=True)
                    MESSAGE=["Message: ", message.decode()]
                    MESSAGE=str(MESSAGE[1])
                if part.get_content_maintype() != 'multipart' and part.get('Content-Disposition') is not None:
                    print ("image content")
                    image = part.get_filename().split('.')
                    image_name =  f"{image[0]}id.{image[1]}"
                    open('img/' + image_name, 'wb').write(part.get_payload(decode=True))
                    return 'img/' + image_name
            if 'daniel' in FROM[1] and 'command' in SUBJECT[1]:
                email_command=(MESSAGE.replace('\\r\\n',''))
                email_command=email_command.lower()
                return email_command
    
    def Send(self,emailTo,body):
        #Defult subject
        subject="Emma Mail"
        #Make email
        em=EmailMessage()
        em["From"]=self.emailFrom
        em["To"]=emailTo
        em["Subject"]=subject
        em.set_content(body)
        
        context=ssl.create_default_context()
        #send email
        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as smtp:
            smtp.login(self.emailFrom,self.password)
            smtp.sendmail(self.emailFrom,emailTo,em.as_string())
 

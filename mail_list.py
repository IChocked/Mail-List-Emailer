# Make sure to allow LESS SECURE APPS in the security preferences before sending
	# https://myaccount.google.com/security

import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#For the gmail TSL Port
SERVER_ADDRESS = 'smtp.gmail.com'
SERVER_PORT = 587

def get_emails(file, column):
	data_frame = pd.read_csv(file)
	#need to change to work for column specified, not just "Email" column
	return data_frame.Email
	

def get_message_body(file_name):
	file = open(file_name)
	# MAY HAVE TO FORMATE IT AND REPLACE THE \n's
	data = file.read()
	file.close()
	return data;
	
	
def add_attachment(message, file):
	attachment = open(file, "rb")
	
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % file)
 
	message.attach(part)
	return message

	
def generate_message(body, from_address, to_address, subject, attachment_file):
	message = MIMEMultipart()

	message['From'] = from_address
	message['To'] = to_address
	message['Subject'] = subject
	
	message.attach(MIMEText(body, 'plain'))	
	if attachment_file is not 'NO':
		message = add_attachment(message, attachment_file)
	return message
	
	
def send_message(server, message, body, from_add, to_add):
	server.sendmail(from_add, to_add, message.as_string())

def test():
	get_emails("emails.csv", 3)

def main():
	print("got to here")
	my_email = input("Enter your gmail email: ")
	my_pass = input("Enter your password: ")
	
	# Create the server reference
	server = smtplib.SMTP(SERVER_ADDRESS, SERVER_PORT)
	server.starttls()
	# Try logining in 
	try: 
		server.login(my_email, my_pass)
	except:
		print("please allow less secure apps in the security prefernces of your google account: https://myaccount.google.com/security")
	
	email_file = input("enter the .csv file that contains the emails (should be in same directory: ")
	column = input("enter the column name that the emails are under (the label in row 0): ")
	emails = get_emails(email_file, column)
	
	message_file = input("enter the .txt file that conatins the message (only includes the message, no subject, to, or from): ")
	body = get_message_body(message_file)
	subject = input("Enter the subject for the email: ")
	
	attachment_file = input("If you have a file (text, pdf, image, audio, or video), enter the file name with extension below, and if you don't please type 'NO'")
		
	
	# Go through and send the email to everyone on the list
	for email in emails:
		message = generate_message(body, my_email, email, subject, attachment_file)
		send_message(server, message, body, my_email, email)
	server.quit()
	


#gmail smtp settings: port = 587 (TLS), server address = smtp.gmail.com

if __name__ == '__main__':
    main()




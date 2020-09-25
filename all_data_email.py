#!/usr/bin/python
## AUTHOR = kjm
# Usage : python2 all_data_email.py -h

import smtplib
import argparse
import os
from hurry.filesize import size, si

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

parser=argparse.ArgumentParser()
parser.add_argument('-s','--service', help='write service ID')
parser.add_argument('-n','--address',help='write Registered E-mail address, ex:kjm')
parser.add_argument('-p','--put_add', help='put the name(initial),e-mail address separated by Comma,ex: kjm,jmkim@pentamedix.com')
args=parser.parse_args()


###e-mail address
try:
	format_test=args.put_add.spilit(',')
	fa=open('/home/jmkim/Script/Side_task/e-mail_address.txt','a')
	if len(format_test)==2:
		fa.write('\n'+args.put_add)
		fa.close()
	else:
		print 'put the name(initial),e-mail address separated by Comma,ex: kjm,jmkim@pentamedix.com'
except:
	pass

fr=open('/home/jmkim/Script/Side_task/e-mail_address.txt','r')

for i in fr.xreadlines():
	i=i.strip().split(',')
	if args.address == i[0]:
		sender=i[1]
		receiver=i[1]

cmd_list='ls * > fastq_list.txt'
os.system(cmd_list)
fr=open('fastq_list.txt','r')
link=''
link_linux=''
for i in fr.xreadlines():
	i=i.rstrip()
	text='<a href="ftp://Pentamedix:pentamedix@220.78.192.9/Download/{0}">{0}</a>'.format(i)  # second {0} is link name, '>{0}' is redirection
	text2='<a href="ftp://Pentamedix:pentamedix@220.78.192.9/Download/{0}">ftp://Pentamedix:pentamedix@220.78.192.9/Download/{0}</a>'.format(i)
	f_size=os.path.getsize(i)
	f_size=size(f_size, system=si)
	link+=text+'\t'+str(f_size)+'<br>'
	link_linux+='wget'+' '+text2+'\t'+str(f_size)+'<br>'

html='''<html>
  <head></head>
  <body>
    <p>{0}<br><br>
	{1}
    </p>
  </body>
</html>
'''.format(link,link_linux)

msg = MIMEMultipart('alternative')
msg['Subject'] = "This is data link to send"
msg['From'] = sender
msg['To'] = receiver

part2=MIMEText(html,'html',_charset="utf-8")
msg.attach(part2)
s=smtplib.SMTP('localhost')
s.sendmail(sender,receiver,msg.as_string())

os.system('rm fastq_list.txt')

'''message=MIMEText(link,'html')
message['Subject']='test'
message['From']=sender
message['To']=receiver

s=smtplib.SMTP('localhost')
s.sendmail(sender,[receiver],message.as_string())'''

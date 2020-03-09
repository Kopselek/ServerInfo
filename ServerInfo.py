import paramiko
import os
import datetime
from pathlib import Path

Path("logs").mkdir(parents=True, exist_ok=True)

data = ''
with open('config.txt', 'r') as file:
    data = file.read()

dataList = data.splitlines()

hostname = dataList[0]
hostname = hostname.replace('ip:','')

port = dataList[3]
port = port.replace('port:','')

username = dataList[1]
username = username.replace('login:','')

password = dataList[2]
password = password.replace('password:','')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname,port=port,username=username, password=password)
stdin, stdout, stderr = ssh.exec_command('vmstat')

print('Connected to',hostname)

stdout = stdout.readlines()
output = ""

for line in stdout:
    output=output+line
print(output)

print('Saving to the text file into logs folder')

today = datetime.date.today()
time = datetime.datetime.now().time()

file_name = 'logs/' + str(today) + '.txt'
f = open(file_name, 'a+')
f.write('log created: ')
f.write(str(time))
f.write("\n")
f.write(output)
f.close()


quit()
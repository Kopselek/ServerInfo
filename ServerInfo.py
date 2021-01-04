import paramiko
import os
import json
import datetime
from pathlib import Path

Path("logs").mkdir(True, True)

with open('config.json') as json_file:
    data = json.load(json_file)
    for d in data:
        hostname = data['hostname']
        port = int(data['port'])
        username = data['username']
        password = data['password']

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("Connecting to " + hostname + ":" + port)
ssh.connect(hostname, port, username, password)
command = "vmstat -s | awk  ' $0 ~ /total memory/ {total=$1 } $0 ~/free memory/ {free=$1} $0 ~/buffer memory/ {buffer=$1} $0 ~/cache/ {cache=$1} END{print (total-free-buffer-cache)/total*100}'"
stdin, stdout, stderr = ssh.exec_command(command)

print('Connected to - ', hostname)

stdout = stdout.readlines()
output = ""

for line in stdout:
    output=output+line

print('Saving to the text file into logs folder')

today = datetime.date.today()
time = datetime.datetime.now().time()

file_name = 'logs/' + str(today) + '.txt'
f = open(file_name, 'a+')
f.write('============================')
f.write("\n")
f.write('log created: ')
f.write(str(time))
f.write("\n")
f.write("RAM usage in percent: ")
f.write(output)
f.close()

print("Saved")
quit()
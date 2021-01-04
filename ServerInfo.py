import paramiko
import os
import json
import datetime
from pathlib import Path

hostname = ""
port = ""
username = ""
password = ""
output = ""

def create_config():
    print("Creating config file")
    data = []
    data.append({
        'hostname': '127.0.0.1',
        'port': "22",
        'username': 'root',
        'password': 'root'
    })

    with open('config.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    print("Created")

def check_path():
    if not Path("logs").exists():
        print("Creating 'logs' dir")
        Path("logs").mkdir(True, True)
        print("Created")

def connect():
    with open('config.json') as json_file:
        data = json.load(json_file)
        for d in data:
            hostname = d['hostname']
            port = d['port']
            username = d['username']
            password = d['password']
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print("Connecting to - " + hostname + ":" + port)
    ssh.connect(hostname, int(port), username, password)
    command = "vmstat -s | awk  ' $0 ~ /total memory/ {total=$1 } $0 ~/free memory/ {free=$1} $0 ~/buffer memory/ {buffer=$1} $0 ~/cache/ {cache=$1} END{print (total-free-buffer-cache)/total*100}'"
    stdin, stdout, stderr = ssh.exec_command(command)

    print('Connected to - ', hostname + ":" + port)

    stdout = stdout.readlines()
    output = ""

    for line in stdout:
        output = output + line

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


def main():
    try:
        check_path()
        connect()

    except IOError:
        create_config()

if __name__ == '__main__':
    main()
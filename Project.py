import datetime
import socket
import subprocess

password = "Train1ng$"
user = "sysadmin"
host = "192.168.1.10"
cmd = ""

def remoteHomeDir():
    cmd = "ls ~"
    subprocess.Popen(f"echo {password} | ssh {user}@{host} {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def remoteBackup(file):
    cmd = f"cp -v {file} {file}.old"
    subprocess.Popen(f"echo {password} | ssh {user}@{host} {cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

def copyURLDocs(URL):
    print("")

quit = False
while quit == False:
    userInput = input("Please choose an option: \n").upper()
    match userInput:
        case "1":
            print(datetime.datetime.now())
        case "2":
            print(socket.gethostbyname(socket.gethostname()))
        case "3":
            remoteHomeDir()
        case "4":
            userInput = input("Please input the file path: \n")
            remoteBackup(userInput)
        case "5":
            userInput = input("Please provide a valid URL: \n")

            copyURLDocs(userInput)
        case "Q":
            quit = True
            exit
        case _:
            print("Invalid option.")

# Used code from https://stackoverflow.com/questions/3586106/perform-commands-over-ssh-with-python
# used code from https://www.geeksforgeeks.org/python/display-hostname-ip-address-python/
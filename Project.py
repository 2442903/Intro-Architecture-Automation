import datetime
import socket
import subprocess

password = "Train1ng$"
user = "sysadmin"
host = "192.168.1.10"
remote = f"echo {password} | ssh {user}@{host}"

def userInput(msg):

in = input(msg)
return in

def exeCLICommand(cmd):

"""

Execute a CLI command and pipe the results to the Command line interface.

Parameters:

- cmd (str): The CLI command to execute.

"""
try:

# execute the command and pipe the results to the CLI

    subprocess.Popen(f"{cmd}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

except Exception as e:

# if an exception occurs, print the exception message as an error

print("An error has occurred:\n", str(e))

def remoteHomeDir():
    CMD = remote + " ls ~"
    exeCLICommand()

def remoteBackup(file):
    CMD = remote + f"cp -v {file} {file}.old"
    exeCLICommand()

def copyURLDocs(URL):
    cmd = f""

quit = False
while quit == False:

    match input("Please choose an option: \n").upper():
        case "1":
            print(datetime.datetime.now())
        case "2":
            print(socket.gethostbyname(socket.gethostname()))
        case "3":
            remoteHomeDir()
        case "4":
            remoteBackup(userInput("Please input the file path: \n"))
        case "5":
            copyURLDocs(userInput("Please provide a valid URL: \n"))
        case "Q":
            quit = True
            exit
        case _:
            print("Invalid option.")
""" 
Used code from
 https://stackoverflow.com/questions/3586106/perform-commands-over-ssh-with-python
 https://www.geeksforgeeks.org/python/display-hostname-ip-address-python/

https://brightdata.com/blog/how-tos/wget-with-python

"""

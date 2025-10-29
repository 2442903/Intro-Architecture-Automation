import datetime
import socket
import subprocess

password = "Train1ng$"
user = "sysadmin"
host = "192.168.1.10"
remote = f"echo {password} | ssh {user}@{host}"

def cleanUserInput(msg):

    """

    Sanitize user input before returning the data.

    Parameters:

    - msg (str): user generated string to be sanitized.

    """

    data = input(msg)

    return data

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

    """

    Perform the "ls ~" in a remote terminal and pipe the results of the command to the local machine.

    """

    new_cmd = remote + " ls ~"
    exeCLICommand(new_cmd)

def remoteBackup(file):

    """

    Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

    Parameters:

    - file (str): The location and name of a remote file. 

    """

    new_cmd = remote + f"cp -v {file} {file}.old"
    exeCLICommand(new_cmd)

def copyURLDocs(url):

    """

    Download the web documents of the user given url.

    Parameters:

    - url (str): The target webpage which the user has entered to scrape.

    """

    new_cmd = f""
    exeCLICommand(new_cmd)

quit = False
while quit == False:

    """

    Simple while loop to maintain a CLI menu 

    Runs indefinately until the user enters "q" or "Q" into the terminal

    """

    match cleanUserInput("Please choose an option: \n").upper():

        case "1":

            # Print the local date and time of the host machine. 
            # Format: yyyy-mm-dd hh:mm:ss.{milliseconds}

            print(datetime.datetime.now())

        case "2":

            # Get the private ip address by way of getting the host socket information.
            # Potential faliure case: if there is no internet connection expect the return of the loopback address instead.

            print(socket.gethostbyname(socket.gethostname()))

        case "3":

            # Perform the "ls ~" in a remote terminal and pipe the results of the command to the local machine.

            remoteHomeDir()

        case "4":

            # Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

            remoteBackup(cleanUserInput("Please input the file path: \n"))

        case "5":

            # Download the web documents of the user given url.

            copyURLDocs(cleanUserInput("Please provide a valid URL: \n"))

        case "Q":

            # Quit the menu and end the program.

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

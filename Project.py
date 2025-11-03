import datetime
import socket
from colors import colorize
try:
    import pexpect
except Exception as e:
    print(colorize("FAIL", str(e)))
import urllib.request

class userLogin:
    PASSWORD = "Train1ng$"
    USER = "sysadmin"
    REMOTE_IP = "192.168.1.86"
    REMOTE_CMD = f"ssh {USER}@{REMOTE_IP}"

def cleanUserInput(msg: str, type_case = ""):

    """

    Sanitize user input before returning the data.

    Parameters:

    - msg (str): user generated string to be sanitized.
     
    - type_case (char): select how to format the characters in the msg string (e.g. 'U' = upper, 'L' = lower)

    Returns:

    - data (str): user input that has been modified to cause fewer issues

    """

    # Strip leading and trailing spaces
    data = input(colorize("OKCYAN", msg)).strip()

    # If need be standardize the input to a specifiic case.
    match type_case.upper():
        case "U":
            return data.upper()
        case "L": 
            return data.lower()
        case _:
            return data

    

def exeCLICommand(cmd: str, remote = False):

    """

    Spawn a child process to run CLI commands and print the output to the terminal.

    Parameters:

    - cmd (str): The CLI command to execute.

    - remote (bool): Executes the command on a remote machine if true (Default: False)

    """

    try:

        # Spawn a CLI subprocess to handle input
        ssh = pexpect.spawn(cmd)

        # If executing code on a remote terminal, 
        # Wait for the machine to request the password and pass it through.
        if (remote == True):
            ssh.expect("password:")
            ssh.sendline(userLogin.PASSWORD)
        
        # Directly output by using a print function once child process has concluded.
        ssh.expect(pexpect.EOF)
        print(ssh.before.decode("utf-8"))

    except Exception as e:

        # If an exception occurs, print the exception message as an error
        print(colorize("FAIL", "An error has occurred:\n" + str(e)))

def remoteHomeDir():

    """

    Perform the "ls ~" in a remote terminal and pipe the results of the command to the local machine.

    """

    # Append the command for listing the home directory to the remote ssh command then,
    # Execute the new command though the CLI function as a remote execution 
    new_cmd = userLogin.REMOTE_CMD + " ls ~"
    exeCLICommand(new_cmd, True)

def remoteBackup(file: str):

    """

    Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

    Parameters:

    - file (str): The location and name of a remote file. 

    """

    # Append the command for backing up a file to the remote ssh command then,
    #  pass to the execute function as a remote execution
    new_cmd = userLogin.REMOTE_CMD + f" cp -v {file} {file}.old"
    exeCLICommand(new_cmd, True)

def copyURLDocs(url: str):

    """

    Download the web documents of the user given url.

    Parameters:

    - url (str): The target webpage which the user has entered to scrape.

    """

    # By default the program only scrapes the .html,
    # and saves it at the execution directory as the name it wass scraped as.
    flags_str = str("")

    if cleanUserInput("\nDo you wish to change any of the default options? [y/N]\n", "u") == "Y":

        if cleanUserInput("Do you wish to download only HTML? [Y/n]\n", "u")== "N":

            # Recursively download the site with a depth of one and preserve links to maintain webpage funtionality offline.
            print(colorize("OKCYAN", "Download all webpage data..."))
            flags_str += "--recursive --level=1 --convert-links "

        # Only offer to change the name of the download in the case that ONLY the .html is being downloaded.
        elif cleanUserInput("Do you wish to chnage the name of the download? [y/N]\n", "u") == "Y":

            # Have Wget rename the index.html to the user generated input.
            file_name = cleanUserInput("Please provide a name for the download:\n")
            flags_str += "--output-document=" + file_name

    # This is mutally exclusive with changing the document name and downloading more than the html
    if (flags_str == ""):

            # If enabled Wget only downloads a copy, if the file timestamp has changed.           
            # May not work on certain websites due to a lack of a timestamp. (e.g. Google.com)
            print(colorize("OKCYAN", "Using default options..."))
            flags_str += "--timestamping "

    exeCLICommand(f"wget {flags_str} {url}")   

quit = False
while quit == False:

    """

    Simple while loop to maintain a CLI menu.
    Runs indefinately until the user enters "q" or "Q" into the terminal.

    """
    
    match cleanUserInput(colorize("OKBLUE", "Please choose an option:\n") +
                        colorize("OKCYAN",  "1)Show date and time (local computer)\n"  + 
                                            "2)Show IP address (local computer)\n" + 
                                            "3)Show remote home directory listing\n" +
                                            "4)Backup remote file\n" +
                                            "5)Save web page\n") +
                        colorize("WARNING", "Q) Quit\n"), "u"):

        case "1":

            # Print the local date and time of the host machine. 
            # Format: yyyy-mm-dd hh:mm:ss

            print(colorize("OKCYAN", "\nThe current Date and Time:\n") + str(datetime.datetime.now().replace(microsecond = 0)), "\n")         

        case "2":

            # Get the private ip address by way of getting the host socket information.
            # Potential faliure case: if there is no internet connection expect the return of the loopback address instead.

            print(colorize("OKCYAN", "\nYour private IP Address is:\n") + str(socket.gethostbyname(socket.gethostname())))

            # To Check Public IP
            print(colorize("OKCYAN", "\nYour puiblic IP Address is:\n") + str(urllib.request.urlopen("https://checkip.amazonaws.com").read().decode("utf-8")))

        case "3":

            # Perform the "ls ~" in a remote terminal and pipe the results of the command to the local machine.

            print(colorize("OKCYAN", "\nRemote Home Directory listing:"))
            remoteHomeDir()

        case "4":

            # Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

            remoteBackup(cleanUserInput("\nPlease input the file path: \n"))

        case "5":
            
            # Download the web documents of the user given url.
            copyURLDocs(cleanUserInput("\nPlease provide a valid URL: \n"))

        case "Q":

            # Quit the menu and end the program.

            print(colorize("WARNING","\nShutdown..."))
            quit = True
            exit

        case _:

            #Defualt case should catch as misinputs or invalid strings.
            print(colorize("WARNING", "\nInvalid option.\n"))

""" 

Used code from

    https://www.geeksforgeeks.org/python/display-hostname-ip-address-python/

    https://brightdata.com/blog/how-tos/wget-with-python

    https://www.baeldung.com/linux/ssh-scp-password-subprocess

"""

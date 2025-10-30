import datetime
import socket
import pexpect

password = "Train1ng$"
USER = "sysadmin"
REMOTE_IP = "192.168.1.86"
REMOTE_CMD = f"ssh {USER}@{REMOTE_IP}"

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def colorize(color: bcolors, message: str):

    """
     
    Add specific formatting characters to a given string.

    Parameters:

    - color (bcolors): formatting attribute from a predefined list of characters.

    - message (str): string to be prepended and appended with formatting.

    """

    # Add formatting characters to the beginning and end of a string.
    # Character specified by passed through attribute.
    return  getattr(bcolors, color.upper()) + message + bcolors.ENDC

def cleanUserInput(msg: str, type_case = ""):

    """

    Sanitize user input before returning the data.

    Parameters:

    - msg (str): user generated string to be sanitized.

    """
    
    data = input(colorize("OKCYAN", msg))

    match type_case:
        case "u":
            return data.upper()
        case "l": 
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
        # wait for the machine to request the password and pass it through.
        if (remote == True):
            ssh.expect("password:")
            ssh.sendline(password)
        
        # direct output by using a print function once concluded.
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
    #  pass to the execute function as a remote execution
    new_cmd = REMOTE_CMD + " ls ~"
    exeCLICommand(new_cmd, True)

def remoteBackup(file: str):

    """

    Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

    Parameters:

    - file (str): The location and name of a remote file. 

    """

    # Append the command for backing up a file to the remote ssh command then,
    #  pass to the execute function as a remote execution
    new_cmd = REMOTE_CMD + f" cp -v {file} {file}.old"
    exeCLICommand(new_cmd, True)

def copyURLDocs(url: str, html_only = True, file_dir = "", file_name = ""):

    """

    Download the web documents of the user given url.

    Parameters:

    - url (str): The target webpage which the user has entered to scrape.

    - file_dir (str): Optional input for setting the destination of the scraped files

    - file_name (str): Optional input for setting the file name of the Scraped files

    """

    optional_flags = {}
    flags_str = ""

    # Add flags for recursion, set the depth to 1, and convert links to maintain webpage funtionality offline.
    if (html_only == False):
        flags_str += "--recursive --level=1 --convert-links"

    # Change dir flag:
    if (file_dir != ""):
        optional_flags["--directory-prefix="] = file_dir

    # Output doc name flag:
    if (file_name != ""):
        optional_flags["--output-document="] = file_name
    else:
        # Add the -N flag to ensure the Wget command only downloads a copy of the webpage if the file timestamp has changed.
        # This is mutally exclusive with changing the document name.
        flags_str += "--timestamping"

    # Form the key value pairs into a string for use in the wget command if present.
    if (len(optional_flags) != 0):
        for key in optional_flags:
            flags_str += str(key + optional_flags[key])

    # Create the final command to pass to the execute function.
    cmd = f"wget {flags_str} {url}"

    exeCLICommand(cmd)   

quit = False
while quit == False:

    """

    Simple while loop to maintain a CLI menu.
    Runs indefinately until the user enters "q" or "Q" into the terminal.

    """

    print(colorize("OKBLUE",  "Please choose an option:\n") +
          colorize("OKCYAN",  "1)Show date and time (local computer)\n"  + 
                              "2)Show IP address (local computer)\n" + 
                              "3)Show remote home directory listing\n" +
                              "4)Backup remote file\n" +
                              "5)Save web page\n") +
          colorize("WARNING", "Q) Quit\n"))
    
    match cleanUserInput("", "u"):

        case "1":

            # Print the local date and time of the host machine. 
            # Format: yyyy-mm-dd hh:mm:ss.{milliseconds}

            print(colorize("OKCYAN", "\nThe current Date and Time:\n") + str(datetime.datetime.now()), "\n")

        case "2":

            # Get the private ip address by way of getting the host socket information.
            # Potential faliure case: if there is no internet connection expect the return of the loopback address instead.

            print(colorize("OKCYAN", "\nYour private IP Address is:\n") + str(socket.gethostbyname(socket.gethostname())), "\n")

        case "3":

            # Perform the "ls ~" in a remote terminal and pipe the results of the command to the local machine.

            print(colorize("OKCYAN", "\nRemote Home Directory listing:"))
            remoteHomeDir()

        case "4":

            # Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

            remoteBackup(cleanUserInput("\nPlease input the file path: \n"))

        case "5":
            
            # By default the program only scrapes the .html and saves it at the execution directory as index.html
            answer_html = True
            dir = ""
            name = ""

            if cleanUserInput("\nDo you wish to change any of the default options? [y/N]\n", "u") == "Y":

                if cleanUserInput("Do you wish to download only HTML? [Y/n]\n", "u")== "N":

                    # This is if the user wishes to download more than just the .html
                    # Recursively download the site with a depth of one and preserve links.
                    answer_html = False

                # Only offer to change the name of the download in the case that ONLY the .html is being downloaded.
                elif cleanUserInput("Do you wish to chnage the name of the download? [y/N]\n", "u") == "Y":

                    # This is only if the user chooses to download ONLY the .html
                    # Have Wget rename the index.html to the user generated input.
                    name = cleanUserInput("Please provide a name for the download:\n")

                if cleanUserInput("Do you wish to change the download location? [y/N]\n", "u") == "Y":

                    # Have Wget download the file to the user generated folder.
                    dir = cleanUserInput("Please provide the desired download folder:\n")
                
            # Download the web documents of the user given url.
            copyURLDocs(cleanUserInput("\nPlease provide a valid URL: \n"), answer_html, dir, name)

        case "Q":

            # Quit the menu and end the program.

            print(colorize("WARNING","\nShutdown..."))
            quit = True
            exit

        case _:

            print(colorize("WARNING", "\nInvalid option.\n"))

""" 

Used code from

    https://www.geeksforgeeks.org/python/display-hostname-ip-address-python/

    https://brightdata.com/blog/how-tos/wget-with-python

    https://www.baeldung.com/linux/ssh-scp-password-subprocess

"""

import datetime
import urllib.request
import urllib.error
import socket
import sys
from colors import colorize

# Attempt to import paramiko, as it's the only non-standard library.

try:
    import paramiko
except ImportError:
    print(colorize("FAIL", "FATAL ERROR: The 'paramiko' library is required."))
    print(colorize("WARNING", "Please install it using: pip install paramiko"))
    sys.exit(1)


class userLogin:
    PASSWORD = "Train1ng$"
    USER = "sysadmin"
    REMOTE_IP = "192.168.1.86"
    REMOTE_CMD = f"ssh {USER}@{REMOTE_IP}"

def clean_user_input(msg: str, type_case: str = "") -> str:

    """
    Sanitize user input before returning the data.

    Parameters:
    - msg (str): The prompt message to display to the user.    
    - type_case (char): A flag to control case formatting: (e.g. 'U' = upper, 'L' = lower)

    Returns:
    - str: The sanitized, stripped, and case-formatted user input.

    Raises:
    - SystemExit: If the user triggers a KeyboardInterrupt (Ctrl+C) 
                  or EOFError (Ctrl+D), the program will exit gracefully.
    """

    try:
        # Get input, colorize the prompt, and strip leading/trailing whitespace
        data = input(colorize("OKCYAN", msg)).strip()

        # Standardize the input to a specific case if requested
        match type_case.upper():
            case "U":
                return data.upper()
            case "L":
                return data.lower()
            case _:
                return data

    except (KeyboardInterrupt, EOFError):
        # Handle user interruption (Ctrl+C or Ctrl+D)
        print(colorize("WARNING", "\nInput cancelled by user. Exiting..."))
        sys.exit(1) # Exit the program cleanly
    
def get_local_ip() -> str:

    """
    Get the local IP address by connecting to an external server.
    """

    try:
        # Connect to a well-known external IP (Google's DNS)
        # This doesn't send any data; it just finds the right local interface.
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        return f"Could not determine IP: {e}"

def get_public_ip() -> str:

    """
    Get the public IP address from an external service.
    """

    try:
        with urllib.request.urlopen("https://checkip.amazonaws.com") as response:
            ip = response.read().decode("utf-8").strip()
            return ip
    except urllib.error.URLError as e:
        return f"Could not fetch public IP: {e.reason}"
    
def exe_cli_command(cmd: str, remote: bool = False):

    """
    Spawn a child process to run CLI commands and print the output to the terminal.

    Parameters:
    - cmd (str): The CLI command to execute.
    - remote (bool): Executes the command on a remote machine if true (Default: False)
    """

    #Paramiko implimentation needed here to replace pexpect to resolve issue of linux dependancy

def remote_home_dir():

    """
    Perform the "ls ~" in a remote terminal and pipe the results of the command to the local machine.
    """

    # Append the command for listing the home directory to the remote ssh command then,
    # Execute the new command though the CLI function as a remote execution 
    new_cmd = userLogin.REMOTE_CMD + " ls ~"
    exe_cli_command(new_cmd, True)

def remote_backup(file: str):

    """
    Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

    Parameters:
    - file (str): The location and name of a remote file. 
    """

    # Append the command for backing up a file to the remote ssh command then,
    #  pass to the execute function as a remote execution
    new_cmd = userLogin.REMOTE_CMD + f" cp -v {file} {file}.old"
    exe_cli_command(new_cmd, True)

def copy_url_docs(url: str):

    """
    Download the web documents of the user given url.

    Parameters:
    - url (str): The target webpage which the user has entered to scrape.
    """

    # By default the program only scrapes the .html,
    # and saves it at the execution directory as the name it wass scraped as.
    flags_str = str("")

    if clean_user_input("\nDo you wish to change any of the default options? [y/N]\n", "u") == "Y":

        if clean_user_input("Do you wish to download only HTML? [Y/n]\n", "u")== "N":

            # Recursively download the site with a depth of one and preserve links to maintain webpage funtionality offline.
            print(colorize("OKCYAN", "Download all webpage data..."))
            flags_str += "--recursive --level=1 --convert-links "

        # Only offer to change the name of the download in the case that ONLY the .html is being downloaded.
        elif clean_user_input("Do you wish to chnage the name of the download? [y/N]\n", "u") == "Y":

            # Have Wget rename the index.html to the user generated input.
            file_name = clean_user_input("Please provide a name for the download:\n")
            flags_str += "--output-document=" + file_name

    # This is mutally exclusive with changing the document name and downloading more than the html
    if (flags_str == ""):

            # If enabled Wget only downloads a copy, if the file timestamp has changed.           
            # May not work on certain websites due to a lack of a timestamp. (e.g. Google.com)
            print(colorize("OKCYAN", "Using default options..."))
            flags_str += "--timestamping "

    exe_cli_command(f"wget {flags_str} {url}")   

def main():

    while True:

        """
        Simple while loop to maintain a CLI menu.
        Runs indefinately until the user enters "q" or "Q" into the terminal.
        """
    
        match clean_user_input(colorize("OKBLUE", "Please choose an option:\n") +
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

                # Get local and public IP addresses
                
                print(colors.colorize("OKCYAN", "\nYour private IP Address is: ") + get_local_ip())
                print(colors.colorize("OKCYAN", "Your public IP Address is:  ") + get_public_ip())
                
            case "3":

                # Perform the "ls ~" in a remote terminal and pipe the results of the command to the local machine.

                print(colorize("OKCYAN", "\nRemote Home Directory listing:"))
                remote_home_dir()

            case "4":

                # Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

                remote_backup(clean_user_input("\nPlease input the file path: \n"))

            case "5":
                
                # Download the web documents of the user given url.
                copy_url_docs(clean_user_input("\nPlease provide a valid URL: \n"))

            case "Q":

                # Quit the menu and end the program.

                print(colorize("WARNING","\nShutdown..."))
                break

            case _:

                #Defualt case should catch as misinputs or invalid strings.
                print(colorize("WARNING", "\nInvalid option.\n"))

if __name__ == "__main__":
    main()

""" 

Used code from

    https://www.geeksforgeeks.org/python/display-hostname-ip-address-python/

    https://brightdata.com/blog/how-tos/wget-with-python

    https://www.baeldung.com/linux/ssh-scp-password-subprocess

"""

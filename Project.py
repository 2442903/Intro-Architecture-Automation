import socket
import sys
import subprocess
from datetime import datetime
from urllib import request, error
from shlex import quote
from colors import colors
import standard_input

# Attempt to import paramiko, as it's the only non-standard library.

try:

    import paramiko
    PARAMIKO_AVAILABLE = True

except ImportError:

    print(colors.colorize("The 'paramiko' library was not found.\n" +
                             "Local functions (1, 2, 5) will still work...\n").grey())

    try:
        # Get the permission of the user to attempt the installation of paramiko
        choice = standard_input.std(colors.colorize("Would you like to attempt to install it now? [Y/n] ").cyan(), "U")

    except (KeyboardInterrupt, EOFError):

        choice = "N" # Default to 'No' on interrupt
        
    if choice == "N":

        print(colors.colorize("Running in limited mode. Remote features are disabled.").warning())
        PARAMIKO_AVAILABLE = False

    else:
        # Try to install using the 'pip' module
        print(colors.colorize("Attempting to install 'paramiko' via pip...").cyan())
        
        try:
            # Use 'sys.executable' to ensure we use the pip
            # for the *current* python interpreter.
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "paramiko"],
                capture_output=True,
                text=True,
                check=True # This will raise an exception if pip fails
            )
            
            # Handle Success
            print(colors.colorize("Successfully installed 'paramiko'.").green())
            print(colors.colorize("Please restart the program to enable remote features.").cyan())
            
            # Must exit for Python to recognize the new module.
            sys.exit(0) 

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # Handle Failure
            print(colors.colorize("Installation failed.").fail())

            if hasattr(e, 'stderr') and e.stderr:

                print(e.stderr) # Show pip's error message

            else:

                print(e)
            
            print(colors.colorize("Please install 'paramiko' manually (e.g., 'pip install paramiko')").fail())
            print(colors.colorize("Running in limited mode. Remote features are disabled.").warning())
            PARAMIKO_AVAILABLE = False
class userLogin:
    PASSWORD = "Train1ng$"
    USER = "sysadmin"
    REMOTE_IP = "192.168.1.86"
    REMOTE_MACHINE = f"{USER}@{REMOTE_IP}"
    TIMEOUT = 10

def wait_for_user():

    """
    Wait for the user to hit enter before displaying a menu once again.
    """

    input(colors.colorize("Press Enter to continue...\n").cyan())
    
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
        # Check with AWS to get the public Ip of localhost.
        with request.urlopen("https://checkip.amazonaws.com") as response:
            ip = response.read().decode("utf-8").strip() # The web page only displays your public IP.
            return ip
        
    except error.URLError as e:
        return f"Could not fetch public IP: {e.reason}"
    
def setup_cli() -> paramiko.SSHClient | None:

    """
    Prompt for credentials and establish a Paramiko SSH connection.
    Returns the client object or None on failure.
    """

    try:

        client = paramiko.SSHClient()
        
        # This avoids managing host keys.
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # This is insecure for production, but within the bounds of the assignment it is permissable.
        print(colors.colorize(f"\nConnecting to {userLogin.REMOTE_MACHINE}...").cyan())
        client.connect(userLogin.REMOTE_IP, username = userLogin.USER, password = userLogin.PASSWORD, timeout = userLogin.TIMEOUT)
        print(colors.colorize("Connection Successful!").green())
        return client

    except paramiko.ssh_exception.AuthenticationException: # Failed to log in (e.g., incorrect user or password.)
        print(colors.colorize("\nAuthentication Failed. Check username/password.").fail())
    except paramiko.ssh_exception.NoValidConnectionsError: # Failed to port forward or lost connection to the remote machine.
        print(colors.colorize(f"\nUnable to connect to port 22 on {userLogin.REMOTE_IP}.").fail())
    except socket.timeout: # Failed to return anything in a timely manner.
        print(colors.colorize("\nConnection timed out.").fail())
    except Exception as e: # Default case to catch anything not covered.
        print(colors.colorize(f"\nAn unexpected SSH error occurred: {e}").fail())
        
    return None
    
def cli_results(out: str, err: str,
                success_prefix: str = "",
                error_prefix: str = "Remote error:\n",):
    
    """
    Prints the output and error strings from an SSH command
    with custom formatting and colors.

    Parameters:
    - out (str): The stdout text from the command.
    - err (str): The stderr text from the command.
    - success_prefix (str): Text to prepend to the output (e.Read. "Success:\n").
    - error_prefix (str): Text to prepend to the error (e.g., "Error:\n").

    """

    # Some commands might print warnings to stderr even on success. 
    
    if err:
        message = f"{error_prefix}{err}" if error_prefix else err
        print(colors.colorize(message).warning())
    
    # If there's no error, or if a command prints to both, display their output.

    if out:
        message = f"{success_prefix}{out}" if success_prefix else out
        print(colors.colorize(message).cyan())
    
def exe_cli_command(client: paramiko.SSHClient, command: str) -> tuple[str, str]:

    """
    Executes a command on the remote SSH client and returns the
    decoded, stripped output and error streams.

    Parameters:
    - client (paramiko.SSHClient): The connected SSH client.
    - command (str): The command string to execute.

    Returns:
    - tuple[str, str]: A tuple containing (stdout, stderr).
    """

    try:
        # Execute the command
        stdin, stdout, stderr = client.exec_command(command)

        # IMPORTANT: Wait for the command to finish.
        # This waits until the command is done, ensuring it can read the ENTIRE output.
        exit_status = stdout.channel.recv_exit_status()

        # Read and decode output and error
        out = stdout.read().decode("utf-8").strip()
        err = stderr.read().decode("utf-8").strip()
        
        return out, err

    except Exception as e:
        # Handle exceptions from the execution itself
        err_msg = f"Failed to execute command '{command}': {e}"
        print(colors.colorize(err_msg).fail())
        return "", err_msg # Return empty output and the error message

def remote_home_dir(client: paramiko.SSHClient):

    """
    Perform the "ls -lA ~" in a remote terminal and pipe the results of the command to the local machine.
    """

    # Append the command for listing the home directory to the remote ssh command then,
    # Execute the new command though the CLI function as a remote execution 
    print(colors.colorize("\nRemote Home Directory listing:").cyan())
    
    # Run the command
    out, err = exe_cli_command(client, "ls -lA ~")
    
    # Report the result
    # We use the defaults: no prefix, OKCYAN for out, WARNING for err.
    cli_results(out, err)

def remote_backup(client: paramiko.SSHClient):

    """
    Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.

    Parameters:
    - client (SSHClient): The client object created by the main loop
    """

    # Append the command for backing up a file to the remote ssh command then,
    #  pass to the execute function as a remote execution
    file_path = standard_input.std("\nPlease input the full file path to back up: \n")
    if not file_path:
        print(colors.colorize("No file path provided.").warning())
        return

    print(colors.colorize(f"Attempting to back up '{file_path}'...").cyan())

    safe_path = ""

    if file_path == "~":
        # Handle just the home directory itself
        safe_path = "~"

    elif file_path.startswith("~/"):
        # Path starts with tilde.
        # Get the part AFTER '~/' (e.g., 'my file.txt')
        rest_of_path = file_path[2:]

        # Safely quote ONLY that part.
        safe_rest_of_path = quote(rest_of_path)

        # This creates a safe path like ~/'my file.txt'
        safe_path = "~/" + safe_rest_of_path
    else:
        # Not a home directory path, quote the whole thing.
        safe_path = quote(file_path)
    command = f"cp -v {safe_path} {safe_path}.old"

    # Run the command
    out, err = exe_cli_command(client, command)
    
    # Report the results
    cli_results(out, err,
                        success_prefix="Backup successful:\n",
                        success_color="OKGREEN",
                        error_color="FAIL")

def copy_url_docs(url: str):

    """
    Download the web documents of the user given url.

    Parameters:
    - url (str): The target webpage which the user has entered to scrape.
    """
    # Append http if not present.
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url
        print(colors.colorize(f"Prepending 'https://'. Using URL: {url}").cyan())

    try:
        # Get a default filename from the URL, or use 'index.html'
        default_name = url.split('/')[-1]
        if not default_name or '.' not in default_name:
            default_name = "index.html"
    
        file_name = standard_input.std(f"Enter file name to save '{default_name}' as: ")
        if not file_name:
            file_name = default_name

        print(colors.colorize(f"Downloading content from {url}...").cyan())
        
        # Make a request for the web page and save the data returned.
        with request.urlopen(url) as response:
            content = response.read()

        # Write the content of the web page to a file on the system.    
        with open(file_name, 'wb') as f:
            f.write(content)
            
        print(colors.colorize(f"\nSuccessfully saved page to '{file_name}' ({len(content)} bytes).").green())

    except (error.HTTPError, error.URLError) as e: # Check for issues with a lack of http or a non functional url
        print(colors.colorize(f"\nFailed to retrieve URL: {e.reason}").fail())
    except ValueError as e: # Check for invalid objects when asking for the url
        print(colors.colorize(f"\nInvalid URL: {e}").fail())
    except IOError as e: # Check for any issues writing to a file on the system
        print(colors.colorize(f"\nFailed to write file '{file_name}': {e}").fail())
    except Exception as e: # Default case to catch anything else
        print(colors.colorize(f"\nAn unexpected error occurred: {e}").fail())

def main():

    cli_client = setup_cli()

    while True:

        """
        Simple while loop to maintain a CLI menu.
        Runs indefinately until the user enters "q" or "Q" into the terminal.
        """

        construct_menu = (str(colors.colorize("Please choose an option:\n").blue()) + str(colors.colorize("1) Show date and time (local computer)\n" + "2) Show IP address (local computer)\n").cyan()))
        
        # Only add remote options if paramiko (and thus the client) is available
        if PARAMIKO_AVAILABLE and cli_client:
            construct_menu = (construct_menu + str(colors.colorize("3) Show remote home directory listing\n" + "4) Backup remote file\n").cyan()))
        else:
            construct_menu = (construct_menu + str(colors.colorize("3) Show remote home directory listing\n" + "4) Backup remote file\n").grey()))
        
        construct_menu = (construct_menu + str(colors.colorize("5) Save web page\n").cyan()) + str(colors.colorize("Q) Quit\n").warning()))
    
        match standard_input.std(construct_menu, "U"):

            case "1":

                # Print the local date and time of the host machine. 
                # Format: yyyy-mm-dd hh:mm:ss

                print(colors.colorize("\nThe current Date and Time:\n").cyan() + datetime.now().replace(microsecond = 0) + "\n")         

            case "2":

                # Get local and public IP addresses
                
                print(colors.colorize("\nYour private IP Address is: ").cyan() + get_local_ip())
                print(colors.colorize("Your public IP Address is:  ").cyan() + get_public_ip())
                
            case "3":

                # Perform the "ls -lA ~" in a remote terminal and pipe the results of the command to the local machine.
                if PARAMIKO_AVAILABLE and cli_client:
                    remote_home_dir(cli_client)
                else:
                    print(colors.colorize("\nInvalid option. Remote features are disabled.").fail())
                

            case "4":

                # Perform a simple "cp" command on a remote machine and append the ".old" suffix to the copied file.
                if PARAMIKO_AVAILABLE and cli_client:
                    remote_backup(cli_client)
                else:
                    print(colors.colorize("\nInvalid option. Remote features are disabled.").fail())
                

            case "5":
                
                # Download the web documents of the user given url.
                url = standard_input.std("\nPlease provide a valid URL: \n")
                if url:
                    copy_url_docs(url)
                else:
                    print(colors.colorize("No URL provided.").warning())

            case "Q":

                # Quit the menu and end the program.

                print(colors.colorize("\nShutdown...").warning())
                if cli_client:
                    cli_client.close()
                break

            case _:

                #Defualt case should catch as misinputs or invalid strings.
                print(colors.colorize("\nInvalid option.\n").warning())

        wait_for_user()

if __name__ == "__main__":
    main()

""" 

Used code from

    https://www.geeksforgeeks.org/python/display-hostname-ip-address-python/

    https://brightdata.com/blog/how-tos/wget-with-python

    https://www.baeldung.com/linux/ssh-scp-password-subprocess

"""

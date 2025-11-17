from colors import colors
import sys

def std(msg: str, type_case: str = "") -> str:

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
        data = input(colors.colorize(msg).cyan()).strip()

        # Standardize the input to a specific case if requested
        match type_case.upper():
            case "U":
                return data.upper()
            case "L":
                return data.lower()
            case _:
                return data

    except (KeyboardInterrupt, EOFError): # Handle user interruption (Ctrl+C or Ctrl+D)
        print(colors.colorize("\nInput cancelled by user. Exiting...").warning())
        sys.exit(1) # Exit the program cleanly
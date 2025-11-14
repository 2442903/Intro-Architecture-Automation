class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def colorize(*attributes, message: str) -> str:
        """
        Applies multiple formatting attributes to a message string.

        Parameters:
        - *attributes (str): Variable number of attribute names
                             (e.g., "BOLD", "FAIL", "UNDERLINE").
        - message (str): The string to be formatted. This MUST
                         be passed as a keyword argument.

        Returns:
        - str: The colorized and formatted string.
        
        Example:
        colors.colorize("BOLD", "FAIL", message="This is a bold failure.")
        """
        
        prefix = ""
        for attr in attributes:
            try:
                # Get the ANSI code for the attribute and add it to the prefix
                code = getattr(colors, attr.upper())
                prefix += code
                
            except AttributeError:
                # Handle invalid attribute names
                print(f"(Colorize Warning: Unknown attribute '{attr}')")
        
        # Combine the prefix, message, and the universal reset code
        return f"{prefix}{message}{colors.ENDC}"

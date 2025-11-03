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

    def colorize(color: str, message: str):

        """
        
        Add specific formatting characters to a given string.

        Parameters:

        - color (str): formatting attribute from a predefined list of characters.

        - message (str): string to be prepended and appended with formatting.

        Returns:

        - output (str): colorized text by way of formatting characters at the start and end of the string 

        """

        # Add formatting characters to the beginning and end of a string.
        # Character specified by passed through attribute.
        return  getattr(colors, color.upper()) + message + colors.ENDC

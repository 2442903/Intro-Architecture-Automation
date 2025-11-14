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
    def colorize(color: str, message: str) -> str:

        """        
        Add specific formatting characters to a given string.

        Parameters:
        - color (str): Formatting attribute (e.g., "FAIL", "OKGREEN").
        - message (str): String to be colorized.

        Returns:
        - str: The colorized string.
        """

        # Add formatting characters to the beginning and end of a string.
        # Character specified by passed through attribute.
        try:
            return  getattr(colors, color.upper()) + message + colors.ENDC
        except AttributeError:
            return message # Return unformatted if color name is invalid

class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    GREY = '\033[38;5;8m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    

    @staticmethod
    def colorize(message: str):

        """
        Factory method to create a new _ColorString builder.

        Example:
        print(colors.colorize("My Text").bold().fail())
        """

        return colors._ColorString(message)

    class _ColorString:

        """
        An internal class that holds a string and a list of
        attributes to apply, allowing for method chaining.
        """

        def __init__(self, message: str):
            self._message = message
            self._attributes = []

        def __eq__(self, other):

            """
            Allows Python to compare this object with others based on 
            their final string value (text + ANSI codes).
            """
            
            return str(self) == str(other)

        def __str__(self):

            """
            Generates the final formatted string when printed or cast to str.
            """

            prefix = "".join(self._attributes)
            return f"{prefix}{self._message}{colors.ENDC}"

        def __repr__(self):
            # Represents the object in a way that's useful for debugging
            return f'colors.colorize("{self._message}")' + \
                   "".join([f".{attr[1]}" for attr in self._attributes])

        # Each constant recieves its own method.
        # Each method adds its code and returns 'self' to allow chaining.

        def bold(self):
            self._attributes.append(colors.BOLD)
            return self

        def underline(self):
            self._attributes.append(colors.UNDERLINE)
            return self

        def header(self):
            self._attributes.append(colors.HEADER)
            return self
        
        def grey(self):
            self._attributes.append(colors.GREY)
            return self

        def blue(self):
            self._attributes.append(colors.BLUE)
            return self

        def cyan(self):
            self._attributes.append(colors.CYAN)
            return self

        def green(self):
            self._attributes.append(colors.GREEN)
            return self

        def warning(self):
            self._attributes.append(colors.WARNING)
            return self

        def fail(self):
            self._attributes.append(colors.FAIL)
            return self

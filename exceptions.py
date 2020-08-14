class InvalidInput(Exception):
    """Rasied when a user passes in an invalid input"""

    def __init__(self, value):
        self.value = value
        self.message = f"{value} is not a valid input, please see manual for help"
        super().__init__(self.message)

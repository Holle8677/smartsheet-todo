class UnexpectedColumnsInDatabaseSheet(Exception):
    def __init__(self, message = 'The specified database sheet either contained unexpected columns or was found to be missing expected columns.'):
        self.message = message
        super().__init__(self.message)
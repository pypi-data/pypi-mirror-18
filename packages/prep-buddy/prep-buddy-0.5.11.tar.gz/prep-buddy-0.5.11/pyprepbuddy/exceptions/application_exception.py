class ApplicationException(Exception):
    def __init__(self, java_exception):
        self.java_exception = java_exception

    def message(self):
        return self.java_exception.getMessage()

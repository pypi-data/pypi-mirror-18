import traceback

class ScopetonException(Exception):
    errorText = ""
    parentError = None  # type: Exception

    def __init__(self, errorText, parentError):
        self.errorText = errorText
        self.parentError = parentError
        self.parentStack = traceback.format_exc()

    def __str__(self):
        return "ScopetonException:{e.errorText}\nNested exception:{e.parentError}\n{e.parentStack}".format(e=self)

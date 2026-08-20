"""Application-wide exceptions."""


class CancelEvent(Exception):
    """Raised when the prompt is cancelled."""
    pass

class QuitEvent(Exception):
    """Raised when the user wants to quit or there is nothing more to do."""
    pass

class AppError(Exception):
    """Application error to give feedback to the user."""
    def __str__(self):
        if self.__cause__:
            return f"{super().__str__()}: {self.__cause__}"
        else:
            return super().__str__()

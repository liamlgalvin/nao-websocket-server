from enum import Enum


class ErrorMessage(Enum):
    APP_DOESNT_EXIST = 1
    UNKNOWN_ERROR = 2
    APP_LOCATION_INCORRECT = 3
    APP_ALREADY_RUNNNG = 4
    PROBLEM_RUNNING_APP = 5
    NO_APP_RUNNING = 6
    COULD_NOT_CANCEL_APP = 7
    
    def getMessage(self):
        self.name

class SuccessMessage(Enum):
    APP_STARTED = 1
    APP_FINISHED = 2
    APP_CANCELLED = 3

    def getMessage(self):
        self.name
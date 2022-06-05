from enum import Enum
from domain.app import App


class Status(Enum):
    APP_RUNNING = 1
    NO_APP_RUNNING = 2


class RobotStatus:
    def __init__(self, status: Status, app: App):
        self.status = status,
        self.app = app

    def getDescription(self):
        if self.status == Status.APP_RUNNNING:
            return "{} running".format(self.app.name)
        
        return "no app running".format()
    
    def getStatus(self):
        return self.status[0]
        


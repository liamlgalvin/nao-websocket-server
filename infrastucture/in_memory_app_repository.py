from typing import Set
from domain.app import App
from domain.app_repository import AppRepository

class InMemoryAppRepository(AppRepository):


    inventory = { # this should come from somewhere else ...
        App(1, "first app", "1st app", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/appicons/1.jpg", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/programs/test.py", "python3"),
        App(2, "second app name really long", "2nd app", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/appicons/2.jpg", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/programs/test.py", "python3"),
        App(3, "third app","3rd app", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/appicons/3.jpg", "programs/test.py", "python3"),
        App(4, "family app", "this is an app for all the family", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/appicons/3.jpg", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/programs/test.py", "python3"),
        App(5, "dance app", "this is an app for all the dancers out there, ya ffeeeeeel, this is an app for all the dancers out there, this is an app for all the dancers out there", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/appicons/placeholder.jpg", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/programs/test.py", "python3"),
        App(6, "c app", "this app is written in c", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/appicons/1.jpg", "/home/liam/workspace/websockets/pfg/robotwebsocketserver/test/c.exe", "cpp"),
    }

    def getInventory(self) -> Set:
        return self.inventory
    
    def getInventoryAsDto(self) -> Set:
        global inventory

        temp_set = set()
        
        for value in self.inventory:
            temp_set.add(value.mapToDto())
        return temp_set
    
    def getAppById(self, id: str) -> App:
        for value in self.inventory:
            if str(value.id) == id: 
                return value
        return None

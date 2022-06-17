from typing import Set
from domain.app import App
from domain.app_repository import AppRepository
import requests

REST_SERVER_URI = "http://localhost:8000/"
GET_APP_ENDPOINT = "get-app/"
GET_APPS_ENDPOINT = "get-apps/"

class RestRepository(AppRepository):

    def get_apps(self):
        api_url = REST_SERVER_URI + GET_APPS_ENDPOINT
        response = requests.get(api_url)
        apps:Set = set()

        for jsonApp in response.json():
            app = self.create_app(jsonApp)
            apps.add(app)
        
        return apps

    def getInventory(self) -> Set:
        return self.get_apps()

    
    def getInventoryAsDto(self) -> Set:
        temp_set = set()
        
        for value in self.get_apps():
            temp_set.add(value.mapToDto())
        return temp_set
    
    def getAppById(self, id: str) -> App:
        return self.get_app(id)

    def create_app(self, json):
        return App(id=json['id'],name=json['name'],description=json['description'],image=json['image'],location=json['location'],language=json['language'])

    def get_app(self, id: str):
        api_url = REST_SERVER_URI + GET_APP_ENDPOINT + id
        response = requests.get(api_url)
        app: App = self.create_app(response.json())
        return app

    


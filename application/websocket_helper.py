from email import message
import json

from domain.robot_status import RobotStatus, Status


def reset_connected(websocket, connected):
    connected.remove(websocket)

def get_json_string(app_dict):
    temp_list = []
    for app in app_dict:
        temp_list.append((app.__dict__))
    return temp_list

async def get_apps(websocket, appRepository):
    await websocket.send(json.dumps({"apps": get_json_string(appRepository.getInventoryAsDto())}))


async def send_response(type: str, msg: str, connected, current_app, robot_status):

    app = str(current_app.id) if current_app != None else ""

    message = json.dumps({
            "type": type, 
            "robotStatus": robot_status, # get_robot_status().get_status().name, 
            "currentAppId" : app,
            "message": msg})

    for connection in connected:
        await connection.send(message)

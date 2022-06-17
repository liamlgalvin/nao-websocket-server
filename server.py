#!/usr/bin/env python

import os
from os.path import exists

import asyncio
import signal
import websockets
import json

import socket

from domain.app import App
from infrastucture.rest_repository import RestRepository as AppRepository

from domain.robot_status import RobotStatus, Status
from domain.message import SuccessMessage, ErrorMessage

# run app variables

current_app: App = None
process = None
task = None


connected = []
appRepository = AppRepository()


# run app methods

### use exceptions to send websockets to minimise number of places i am sending??

async def run_app(app: App):

    global process, current_app, task

    if not exists(app.location):
        # reset_global_variables()
        await send_response("error", ErrorMessage.APP_DOESNT_EXIST.name)
        return

    if get_robot_status().getStatus() == Status.APP_RUNNING:
        await send_response("error", ErrorMessage.APP_ALREADY_RUNNNG.name)
        return

    current_app = app
    
    process = await asyncio.create_subprocess_shell(app.getShellCommand(), preexec_fn=os.setsid)

    await send_response("start", SuccessMessage.APP_STARTED.name)

    if(await process.communicate() == (None,None)):

        await send_response("sucess", SuccessMessage.APP_FINISHED.name)
        
    else:

        await send_response("error", ErrorMessage.PROBLEM_RUNNING_APP.name)
    
    reset_global_variables()
    return


async def cancel_app(app):

    global process, task

    print("cancel called")

    if get_robot_status().getStatus() == Status.NO_APP_RUNNING:
        await send_response("error", ErrorMessage.NO_APP_RUNNING.name)
        return

    if get_robot_status().getStatus() == Status.APP_RUNNING: 

        try:
            process.terminate()
            process.kill()
            task.cancel()
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

        except Exception as e:
            await send_response("error", ErrorMessage.COULD_NOT_CANCEL_APP.name)
            return
        
        reset_global_variables()

        await send_response("cancel", SuccessMessage.APP_CANCELLED.name)
        return
    
def get_robot_status() -> RobotStatus:
    if process != None and process.returncode == None:
        return(RobotStatus(Status.APP_RUNNING, current_app))
    return(RobotStatus(Status.NO_APP_RUNNING, current_app))


async def send_response(type: str, msg: str):
    global connected

    app = str(current_app.id) if current_app != None else ""

    for connection in connected: ## maybe I should remove this...
        await connection.send(json.dumps({
            "type": type, 
            "robotStatus": get_robot_status().getStatus().name, 
            "currentAppId" : app,
            "message": msg}))

def reset_global_variables():
    global process
    global current_app
    global task

    task = None
    process = None
    current_app = None

# end run app methods


def get_json_string(app_dict):
    temp_list = []
    for app in app_dict:
        temp_list.append((app.__dict__))
    return temp_list

def reset_connected(websocket):
    global connected
    connected.remove(websocket)

async def get_apps(websocket):
    await websocket.send(json.dumps({"apps": get_json_string(appRepository.getInventoryAsDto())}))


async def handler(websocket):

    global task

    print("A client just connected")
    connected.append(websocket)

    print(connected)
    try:
        async for message in websocket: 

            event = json.loads(message)

            if event["type"] == "cancel":

                asyncio.create_task(cancel_app(current_app))

            elif event["type"] == "start_app":

                id = str(json.loads(event["message"]))

                print(id)
                

                app = appRepository.getAppById(id)

                if app != None:
                    task = asyncio.create_task( run_app(app) )
                else:
                    await send_response("error", ErrorMessage.APP_DOESNT_EXIST.name)

            elif event["type"] == "get_apps": 

                await get_apps(websocket)

            elif event["type"] == "destroy_connection":

                connected.remove(websocket)

            else: 
                await send_response("error", ErrorMessage.UNKNOWN_ERROR.name)

    except websockets.exceptions.ConnectionClosed as e:
        reset_connected(websocket)
    except websockets.exceptions.ConnectionClosedError as e:
        reset_connected(websocket)



async def main():
    hostname = socket.gethostname()
    ip = socket.gethostbyname( "{}.local".format(hostname))
    print("{}:8001".format(ip))
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())





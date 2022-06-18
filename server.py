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
from application.websocket_helper import reset_connected, send_response, get_apps

# run app variables

current_app: App = None
process = None
task = None


connected = []
appRepository = AppRepository()


# run app methods

async def run_app(app: App):

    global process, current_app, task, connected

    if not exists(app.location):
        # reset_global_variables()
        await send_response("error", ErrorMessage.APP_DOESNT_EXIST.name, connected,  current_app, get_robot_status().get_status().name)
        return

    if get_robot_status().get_status() == Status.APP_RUNNING:
        await send_response("error", ErrorMessage.APP_ALREADY_RUNNNG.name, connected,  current_app, get_robot_status().get_status().name)
        return

    current_app = app
    
    process = await asyncio.create_subprocess_shell(app.getShellCommand(), preexec_fn=os.setsid)
    
    # await send_response2("success", "hello", connected,  current_app, get_robot_status().get_status().name)


    await send_response("start", SuccessMessage.APP_STARTED.name, connected,  current_app, get_robot_status().get_status().name)

    if(await process.communicate() == (None,None)):

        await send_response("sucess", SuccessMessage.APP_FINISHED.name, connected,  current_app, get_robot_status().get_status().name)
        
    else:

        await send_response("error", ErrorMessage.PROBLEM_RUNNING_APP.name, connected,  current_app, get_robot_status().get_status().name)
    
    reset_global_variables()
    return


async def cancel_app(app):

    global process, task

    print("cancel called")

    if get_robot_status().get_status() == Status.NO_APP_RUNNING:
        await send_response("error", ErrorMessage.NO_APP_RUNNING.name, connected,  current_app, get_robot_status().get_status().name)
        return

    if get_robot_status().get_status() == Status.APP_RUNNING: 

        try:
            process.terminate()
            process.kill()
            task.cancel()
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)

        except Exception as e:
            await send_response("error", ErrorMessage.COULD_NOT_CANCEL_APP.name, connected,  current_app, get_robot_status().get_status().name)
            return
        
        reset_global_variables()

        await send_response("cancel", SuccessMessage.APP_CANCELLED.name, connected,  current_app, get_robot_status().get_status().name)
        return
    
def get_robot_status() -> RobotStatus:
    if process != None and process.returncode == None:
        return(RobotStatus(Status.APP_RUNNING, current_app))
    return(RobotStatus(Status.NO_APP_RUNNING, current_app))


def reset_global_variables():
    global process, current_app, task

    task = None
    process = None
    current_app = None

# end run app methods


async def handler(websocket):

    global task, connected, current_app, robot_status

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
                    await send_response("error", ErrorMessage.APP_DOESNT_EXIST.name, connected,  current_app, get_robot_status().get_status().name)

            elif event["type"] == "get_apps": 

                await get_apps(websocket, appRepository)

            elif event["type"] == "destroy_connection":

                connected.remove(websocket)

            else: 
                await send_response("error", ErrorMessage.UNKNOWN_ERROR.name, connected,  current_app, get_robot_status().get_status().name)

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





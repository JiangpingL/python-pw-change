import os, sys
import logging

# import the fastapi here
from fastapi import FastAPI

# our module to load the routes
import import_routes

app = FastAPI()

logger = logging.getLogger(__name__)
logger.info('Starting web server ...')

# get the folder from where we load the python modules that contain the routes
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

logger.info("Full path of the FastAPI app module: ", path)
logger.info("Folder of the FastAPI app module: ", dir_path)

routes_path = dir_path + "/routes"
logger.info("Importing modules with routes in folder: ", routes_path)

import_routes.import_routes(app, routes_path)

@app.get("/")
async def welcome() -> dict:
    return {"messsage": "Hello World"}

logger.info('All routes: ', app.routes)



#
# Import all Python files in a folder with each file representing an implementation of password verification/update
# The file name (file_name) will be the name of the endpoint and forms part of the URL path
# The route name is using the convention of {file_name}_route
#

import os
import re
import sys
import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)

#
# Interface
#
def import_routes(app: FastAPI, path: str):
    """ 
    import the routes defined in modules in the folder specified by path
    """
    __import_routes(app, path)


#
# Implementation
#
def __get_module_names_in_dir(path: str):
    """
      Returns a set of all module names residing directly in directory "path".
    """
    result = set()

    # Looks for all python files in the directory (not recursively) and add their name to result:
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            file_name, file_ext = os.path.splitext(entry)
            if file_name != '__init__' and file_ext == '.py': 
                logger.info(f'Found module named: "{file_name}"')
                result.add(file_name)

    return result

def __import_routes(app: FastAPI, path: str):
    """
    import the routes defined in modules in the folder specified by path
    """
    for module_name in __get_module_names_in_dir(path):
        import_name = 'routes.' + module_name
        route_name = module_name + '_routes'
        logger.info(f'Importing module: "{import_name}"')
        module = __import__(import_name, None, None, [route_name])
        route_module = getattr(module, route_name)
        app.include_router(route_module)

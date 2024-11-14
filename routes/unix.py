from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models.target_account import TargetAccount
from models.result import Result
import paramiko
import logging

#
# when loading the routes defined in this module, it is looking for the router object named as {module_name}_routes
#
unix_routes = APIRouter()

# logging in an async program will block the event loop. That is, each call to the logging infrastructure blocks the asyncio
# event loop until the log message is stored in the file. Generally, this is not a concern unless writing to disk is slow or
# there are an enormous number of log messages.
logger = logging.getLogger(__name__)

#
# password verification - synchronous execution, will be run in an external thread pool
#
@unix_routes.post("/unix/verify", status_code=200)
def verify(target_account: TargetAccount, response: JSONResponse) -> Result:

    # get the information from the request
    account_name = target_account.name
    account_pass = target_account.password
    server_host = target_account.target_application.target_server.host
    server_port = target_account.target_application.port

    logger.info(f'Verifying password for Unix user account "{account_name}" on port {server_port} of server "{server_host}"')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # auto add server key

    try:

        client.connect(server_host, port=server_port, username=account_name, password=account_pass)
        logger.info(f'Successfully verified password for Unix user account "{account_name}" on port {server_port} of server "{server_host}"')
        response.status_code = status.HTTP_200_OK
        return Result(success=True, message=f'Successfully verified password for Unix account "{account_name}"')
        
    except Exception as error:

        logger.error(f'Failed to verify password for Unix user account "{account_name}" on port {server_port} of server "{server_host}" with error "{error}"')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
        return Result(success=False, message=f'Failed to verify password for Unix account "{account_name}"')

    finally:

        client.close()

#
# password update - synchronous execution, will be run in an external thread pool
#
@unix_routes.post("/unix/update", status_code=200)
def verify(target_account: TargetAccount, response: JSONResponse) -> Result:

    # get the information from the request
    account_name = target_account.name
    account_pass = target_account.password
    account_new_pass = target_account.new_password
    server_host = target_account.target_application.target_server.host
    server_port = target_account.target_application.port

    logger.info(f'Updating password for Unix user account "{account_name}" on port {server_port} of server "{server_host}"')

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # auto add server key

    try:

        # Connect
        client.connect(server_host, port=server_port, username=account_name, password=account_pass)
        logger.info(f'Successfully connected to server "{server_host}" on port {server_port} with Unix user account "{account_name}"')

        # execute the command to update user password "echo user:password | chpasswd"
        update_command = f'echo {account_name}:{account_new_pass} | chpasswd'
        _stdin, _stdout, _stderr = client.exec_command("uptime")
        command_status = _stdout.channel.recv_exit_status()

        # check the status
        if command_status == 0:
            response.status_code = status.HTTP_200_OK
            return Result(success=True, message=f'Successfully updated password for Unix account "{account_name}"')
        else:
            logger.error(f'Failed to update password for Unix user account "{account_name}" on port {server_port} of server "{server_host}" with error "{error}"')
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
            return Result(success=False, message=f'Failed to update password for Unix account "{account_name}"')
        
    except Exception as error:

        logger.error(f'Failed to update password for Unix user account "{account_name}" on port {server_port} of server "{server_host}" with error "{error}"')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
        return Result(success=False, message=f'Failed to update password for Unix account "{account_name}"')

    finally:

        client.close()
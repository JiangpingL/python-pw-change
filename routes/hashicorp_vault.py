import logging

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from models.target_account import TargetAccount
from models.result import Result

import httpx

#
# when loading the routes defined in this module, it is looking for the router object named as {module_name}_routes
#
hashicorp_vault_routes = APIRouter()

# logging in an async program will block the event loop. That is, each call to the logging infrastructure blocks the asyncio
# event loop until the log message is stored in the file. Generally, this is not a concern unless writing to disk is slow or
# there are an enormous number of log messages.
logger = logging.getLogger(__name__)

# 
# password verification
#
@hashicorp_vault_routes.post("/hashicorp_vault/verify", status_code=200)
async def verify(target_account: TargetAccount, response: JSONResponse) -> Result:

    # get the information from the request
    account_name = target_account.name
    account_pass = target_account.password
    server_host = target_account.target_application.target_server.host
    server_port = target_account.target_application.port

    logger.info(f'Verifying password for HashiCorp Vault user account "{account_name}" on port {server_port} of server "{server_host}"')

    # turn off server certificate verification for now ...
    async with httpx.AsyncClient(verify=False) as client:

        json_payload = '{"password":"' + account_pass + '"}'
        url = 'https://' + server_host + ':' + str(server_port) + '/v1/auth/userpass/login/' + account_name

        logger.info(f'HashiCorp Vault URL for password verification is "{url}"')

        try:
            verify_response = await client.post(url, data=json_payload)
            verify_response.raise_for_status()
            logger.info(f'Password verification returned "{verify_response.json()}"')
            response.status_code = status.HTTP_200_OK
            return Result(success=True, message=f'Successfully verified password for Hashicorp Vault account "{account_name}"')
        except httpx.RequestError as error:
            logger.error(f'Password verification request exception for URL "{url}" - "{error}"')
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
            return Result(success=False, message=f'Failed to verify password for Hashicorp Vault account "{account_name}"')
        except httpx.HTTPStatusError as error:
            logger.error(f'Password verification request returned HTTP status code "{error.response.status_code}" for URL "{url}"')
            response.status_code = error.response.status_code
            return Result(success=False, message=f'Failed to verify password for Hashicorp Vault account "{account_name}" with HTTP status code "{error.response.status_code}" from HashiCorp Vault server')

#
# password update
#
@hashicorp_vault_routes.post("/hashicorp_vault/update", status_code=200)
async def verify(target_account: TargetAccount, response: JSONResponse) -> Result:

    # get the information from the request
    account_name = target_account.name
    account_pass = target_account.password
    account_new_pass = target_account.new_password
    server_host = target_account.target_application.target_server.host
    server_port = target_account.target_application.port

    update_headers = {}

    logger.info(f'Updating password for HashiCorp Vault user account "{account_name}" on port {server_port} of server "{server_host}"')

    # turn off server certificate verification for now ...
    async with httpx.AsyncClient(verify=False) as client:

        # login to obtain a token first
        login_json_payload = '{"password":"' + account_pass + '"}'
        login_url = 'https://' + server_host + ':' + str(server_port) + '/v1/auth/userpass/login/' + account_name
        logger.info(f'HashiCorp Vault URL to login is "{login_url}"')

        try:
            login_response = await client.post(login_url, data=login_json_payload)
            login_response.raise_for_status()

            logger.info(f'Login is successful with the current password')

            # get the token in the response
            auth_token = login_response.json()['auth']['client_token']
            update_headers['X-Vault-Token'] = auth_token

        except httpx.RequestError as error:
            logger.error(f'Password login request exception for URL "{login_url}" - "{error}"')
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
            return Result(success=False, message=f'Failed to login to obtain the auth token for Hashicorp Vault account "{account_name}"')
        except httpx.HTTPStatusError as error:
            logger.error(f'Password login request returned HTTP status code "{error.response.status_code}" for URL "{login_url}"')
            response.status_code = error.response.status_code
            return Result(success=False, message=f'Failed to login to obtain auth token for Hashicorp Vault account "{account_name}" with HTTP status code "{error.response.status_code}" from HashiCorp Vault server')
        
        # now update the password
        update_json_payload = '{"password":"' + account_new_pass + '"}'
        logger.info(f'Update password with auth_token "{auth_token}"')
        update_url = 'https://' + server_host + ':' + str(server_port) + '/v1/auth/userpass/users/' + account_name + '/password'
        logger.info(f'HashiCorp Vault URL to update password is "{update_url}"')

        try:
            update_response = await client.post(update_url, data=update_json_payload, headers=update_headers)
            update_response.raise_for_status()
            logger.info(f'Password update is successful for HashiCorp Vault account "{account_name}"')
            response.status_code = status.HTTP_200_OK
            return Result(success=True, message=f'Successfully updated password for Hashicorp Vault account "{account_name}"')
        except httpx.RequestError as error:
            logger.error(f'Password update request exception for URL "{update_url}" - "{error}"')
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR 
            return Result(success=False, message=f'Failed to update password for Hashicorp Vault account "{account_name}"')
        except httpx.HTTPStatusError as error:
            logger.error(f'Password update request returned HTTP status code "{error.response.status_code}" for URL "{update_url}"')
            response.status_code = error.response.status_code
            return Result(success=False, message=f'Failed to update password for Hashicorp Vault account "{account_name}" with HTTP status code "{error.response.status_code}" from HashiCorp Vault server')
        
        
        
        
        
        
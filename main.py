import configparser

# import the ASGI web server
import uvicorn
# import the app module of the application
import app

# get configurations from configure file config.ini in the same folder
config = configparser.ConfigParser()
config.read('./config.ini')

#print("Configurations: ", config)

# the server address and port number for the web server to listen on
server_host = config['server']['host']
server_port = int(config['server']['port'])

# logging configuration
logging_log_config = config['logging']['logConfig']
logging_access_log = config['logging'].getboolean('accessLog')

# tls configuration
tls_key_file = config['tls']['keyFile']
tls_key_file_pass = config['tls']['keyFilePassword']  # password can be stored in a secret engine and retrieved at the run-time
tls_cert_file = config['tls']['certFile']
tls_ca_certs = config['tls']['caCerts']
tls_cert_reqs = int(config['tls']['certReqs'])

if __name__ == "__main__":
    # uvicorn app:app --host 0.0.0.0 --port 8443 --reload --log-config=./logging.yaml --access-log --ssl-keyfile ./tls/key.pem --ssl-keyfile-password AdminQA1 --ssl-certfile ./tls/cert.pem --ssl-ca-certs ./tls/root.pem
    uvicorn.run(app.app,
                host=server_host,
                port=server_port,
                reload=False,
                log_config=logging_log_config,
                access_log=logging_access_log,
                ssl_keyfile=tls_key_file,
                ssl_keyfile_password=tls_key_file_pass,
                ssl_certfile=tls_cert_file,
                ssl_ca_certs=tls_ca_certs,
                ssl_cert_reqs=tls_cert_reqs)
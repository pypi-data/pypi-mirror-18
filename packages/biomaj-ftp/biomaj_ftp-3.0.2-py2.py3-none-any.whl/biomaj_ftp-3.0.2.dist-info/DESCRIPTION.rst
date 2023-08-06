# Status

In development

# Biomaj ftp

Biomaj FTP server to access production banks

anonymous access is allow with login bank_name and password anonymous.
Existing users can access server with the bank name and their login and API key as password

Only public or allowed banks are accessible

# Config

config.yml contains the server configuration.
Mongo configuration should be the same one than biomaj.

Web endpoint refers to the biomaj API endpoint

# Run

export BIOMAJ_CONFIG=path_to_config.yml

python bin/biomaj_ftp_service.py


3.0.2:
  Allow override of config
  Fix user authentication
  Load database settings from global.properties to match same database than biomaj
3.0.1:
  Fix anonymous access and case where web/local_endpoint is not defined in config.yml
3.0.0:
  FTP server to access banks



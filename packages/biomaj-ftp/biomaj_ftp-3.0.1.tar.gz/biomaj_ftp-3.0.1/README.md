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

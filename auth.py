import starkbank
import os

private_key_path = 'private_key/privateKey.pem'
environment = os.getenv("environment")
id = os.getenv("id")

def _read_private_key_file(private_key_path):
    with open(private_key_path, 'r') as file:
        private_key_content = file.read()
        return private_key_content 

def get_authentication():
    if os.path.isfile(private_key_path):
        private_key_content = _read_private_key_file(private_key_path)
    else:
        print("The previus privateKey.pem file not found.")
        private_key, public_key = starkbank.key.create()
        private_key_content = private_key
    client = starkbank.Project(
        environment=environment,
        id=id,
        private_key=private_key_content
    )
    return client
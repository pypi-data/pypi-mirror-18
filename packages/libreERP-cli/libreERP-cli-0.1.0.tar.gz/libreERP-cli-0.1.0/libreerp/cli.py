import click
import os
import requests
from getpass import getpass

@click.command()
@click.argument('connection', default='', required=True)
@click.argument('action', default='', required=True)
def main(connection,action):
    """My Tool does one thing, and one thing well."""
    parts = connection.split('@')
    username = parts[0]
    server = parts[1]
    password = getpass('Enter your password:')
    sshKey = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()
    r = requests.post("http://" + server + "/api/ERP/registerDevice/",
                json={
                  'username': username,
                  'password': password,
                  'sshKey': sshKey,
                  'mode':action
                }
            )
    if r.status_code ==200:
        outText = 'Success'
    else:
        outText = 'Error'
    click.echo('{0}-: {1} , {2}'.format(r.status_code , outText , server))

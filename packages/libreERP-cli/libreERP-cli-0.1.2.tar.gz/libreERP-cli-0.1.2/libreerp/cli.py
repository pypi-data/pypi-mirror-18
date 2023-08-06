import click
import os
import requests
from getpass import getpass
from ui import getLibreUser , getConfigs , login , uploadSSHKeys




@click.command()
@click.argument('connection', default='', required=True)
@click.option('--action', default='login', required=False , help="action can be either login or logout , default is login")
@click.option('--mode', default='u', required=False , help = "input mode can be ither u means user interface , or a command line c")
@click.option('--proxy', default=None, required=False , help = "provide proxy connection string in the format username:password@server:port")
def main(connection,action , mode , proxy):
    tokenFilePath = os.path.expanduser('~/.libreerp/token.key')



    confs = getConfigs()
    server = None
    if '@' in connection: # means the connection is like username@server:port format
        parts = connection.split('@')
        if len(parts)<2:
            print 'Please provide username@server value or type libreerp --help to know more'
            exit()
        server = parts[1]
        username = parts[0]
    else:
        if confs is None:
            print 'No config.txt found , please provide server address as well in the format username@server:port'
            return
        if mode == 'c':
            username = connection
            server = confs['domain']
        else:
            server = connection


    if confs is None:
        confs = {'domain' : server}
    else:
        if server != '' and '.' in server: # if the server address provided is legitimate one
            confs['domain'] = server
        else:
            print 'The domain: %s is not valid , using the existing server address : %s' %(server , confs['domain'])
    if proxy is not None:
        confs['proxy'] = {
        'http': proxy,
        'https' : proxy,
        }

    confFilePath = os.path.expanduser('~/.libreerp/config.txt')
    f = open(confFilePath , 'w')
    lines = []
    for key in confs:
        if key == 'proxy':
            value = confs[key]['http']
        else:
            value = confs[key]
        if value is None:
            continue
        lines.append('%s=%s\n' % (key , value))
    f.writelines(lines)
    f.close()
    # so far updated the config files



    if mode == 'u':
        # in this mode the user need to provide the url for the ERP not the username@ERP format
        u = getLibreUser()
        print u

    elif mode == 'c':
        # command line mode
        u = getLibreUser(fetchOnly = True)
        print 'in C mode ', u
        if u is None and action == 'logout':
            print 'Cant logout as no user logged in this system'
            return
        if action == 'logout':
            password = getpass('Enter your password:')
            if os.path.isfile(tokenFilePath):
                os.remove(tokenFilePath)
            else:
                print 'No token file to delete , techincally logged out'
            uploadStatus = uploadSSHKeys(u.username , password , action , confs)
            if uploadStatus != 200:
                print 'Retrying SSH key delete'
                uploadStatus = uploadSSHKeys(username , password , action , confs)
                if uploadStatus != 200:
                    print 'Second attempt also failed to delete the SSH keys'
                print 'Logged out successfully'
        else:
            if u is None:
                password = getpass('Enter your password:')
                res = login(username , password)
                if res['status'] == 200:
                    print 'Logged In , uploading the SSH keys now'
                    uploadStatus = uploadSSHKeys(username , password , action , confs)
                    if uploadStatus != 200:
                        print 'Retrying SSH key upload'
                        uploadStatus = uploadSSHKeys(username , password , action , confs)
                else:
                    print res['data']
            else:
                print u

    else:
        click.echo('No mode provided , please provide either c or u for command line or UI respectively')

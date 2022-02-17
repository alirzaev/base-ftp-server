import click

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


@click.command()
@click.option('-p', '--port', type=int, default=21, help='Specify alternate port')
@click.option('-d', '--directory', default='.', help='Specify alternative directory')
@click.option('-u', '--user', required=True, help='Username')
@click.option('--password', required=True, help='Password')
def main(port, directory, user, password):
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    authorizer.add_user(user, password, directory, perm='elradfmwMT')
    authorizer.add_anonymous(directory)

    # Instantiate FTP handler class
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "pyftpdlib based ftpd ready"

    # Instantiate FTP server class and listen on 0.0.0.0:$port
    address = ('0.0.0.0', port)
    server = FTPServer(address, handler)

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # start ftp server
    server.serve_forever()


if __name__ == '__main__':
    main()

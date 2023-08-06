import click

from gh_webhook import Settings, webhook


@click.command()
@click.option(
    '--path',
    default=Settings.path,
    help='Path to repository (Default: {})'.format(Settings.path)
)
@click.option(
    '--command',
    default=Settings.command, help='Command to be executed (Default: {})'.format(Settings.path)
)
@click.option(
    '--port', default=Settings.port,
    help='Port web hook will be using (Default: {})'.format(Settings.port)
)
@click.option(
    '--debug / --no-debug', default=Settings.debug,
    help='Enables debug mode (Default: {})'.format(Settings.debug)
)
@click.option(
    '--secret', default=Settings.secret,
    help='Secret configured in webhook settings (Default: {})'.format(Settings.secret)
)
def init(path, command, port, debug, secret):
    webhook(path=path, command=command, port=port, debug=debug, secret=secret)

if __name__ == '__main__':
    init()

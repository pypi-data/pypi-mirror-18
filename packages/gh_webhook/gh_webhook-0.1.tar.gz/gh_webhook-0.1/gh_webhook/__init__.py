from bottle import run, request, error, post

import logging
import os


class Settings:
    path = '.'
    port = 8080
    command = 'git pull'
    debug = False


@error(404)
def error404(error):
    return 'Document not found'


@post('/')
def index():

    if Settings.debug:
        logging.debug('Request')
        logging.debug(request.forms.__dict__)

    if not request.forms.get('payload'):
        return error404(error)
    os.system("cd {} && {}".format(Settings.path, Settings.command))


def webhook(path=Settings.path, command=Settings.command, port=Settings.port, debug=Settings.debug):
    Settings.path = path
    Settings.command = command
    Settings.port = port
    Settings.debug = debug

    if Settings.debug:
        logging.basicConfig(level=logging.DEBUG)

    run(host='0.0.0.0', port=Settings.port, debug=Settings.debug)

#_webhook = _webhook
import click
from rino import config

def set(path):
    if path.startswith('/'):
        path = path[1:]

    if config.set('remote', path):
        click.echo('remote path set to %s' % path)

def unset():
    if config.set('remote', None):
        click.echo('remote path is unset')

def list():
    if config.get('remote'):
        click.echo('remote path is %s' % config.get('remote'))
    else:
        click.echo('no remote path set')

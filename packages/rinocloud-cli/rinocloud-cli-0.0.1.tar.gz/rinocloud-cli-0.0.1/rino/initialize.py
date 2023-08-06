from rino import config
import click
import json
import os


def initialize():
    cwd = os.getcwd()

    config_path = config.get_config_path()

    if not os.path.exists(config_path):
        with open(config_path, 'w') as outfile:
            outfile.write(json.dumps(config.default_config))
            click.echo('Initialized rino repo in %s' % cwd)
    else:
        click.echo('Reinitialized rino repo in %s' % cwd)

import os
import json
import click
from rino import utils


def show(path):
    metadata, mfile_path = utils.get_notebook_meta(path)

    if not metadata:
        click.echo('No meta information for this notebook (could not find file %s)' % mfile_path)
        return

    if "git" not in metadata.keys():
        click.echo('No git information stored for this notebook')
        return

    git_info = metadata["git"]
    click.echo('git info for %s' % path)
    click.echo('remote: %s %s' % (git_info["remote_name"], git_info["remote_urls"][0]))
    click.echo('branch: %s' % git_info["branch"])
    click.echo('commit: %s' % git_info["commit"])

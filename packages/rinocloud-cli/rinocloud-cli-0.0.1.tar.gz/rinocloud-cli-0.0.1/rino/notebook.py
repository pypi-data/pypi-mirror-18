from git import Repo
from git.exc import InvalidGitRepositoryError
import os
import json
import click
import requests
import rinocloud
from rino import config, login, utils


def delete_rinocloud_object(id):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        return requests.post(rinocloud.api_base + 'files/delete/', json={
            'id': id
        }, headers=headers)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError("Could not connect to specified domain %s" % rinocloud.api_domain)


def push(path, force=False):
    remote = config.get('remote')

    if not remote:
        click.echo('Remote not set. Use `rino remote set <rinocloud_path>` to set the target directory.')
        return

    token = login.get_token()
    rinocloud.api_key = token
    rinocloud.set_local_path(os.getcwd())

    r = rinocloud.Object()
    r.set_name(path, overwrite=True)

    repo = utils.get_git_repo()

    if repo and repo.is_dirty() and not force:
        click.echo('Refusing to push without --force because git repo is dirty')
        return

    git_metadata = utils.get_git_meta(repo)
    if git_metadata:
        r.git = git_metadata

    rinoFolderId = utils.get_rino_folder(rinocloud, remote).json()
    r._parent = rinoFolderId['id']
    r.calculate_etag()
    query = rinocloud.Query().filter(name=r.name, parent=r._parent).query()

    if len(query) > 0:
        click.echo('File already exists on Rinocloud. Use `rino notebook update` to update a file.')
        return
    else:
        click.echo('Pushing %s to %s' % (path, remote))
        utils.save_notebook_meta(path, r)
        r.upload()


def update(path, force=False):
    remote = config.get('remote')

    if not remote:
        click.echo('Remote not set. Use `rino remote set <rinocloud_path>` to set the target directory.')
        return

    token = login.get_token()
    rinocloud.api_key = token
    rinocloud.set_local_path(os.getcwd())

    r = rinocloud.Object()
    r.set_name(path, overwrite=True)

    rinoFolderId = utils.get_rino_folder(rinocloud, remote).json()
    r._parent = rinoFolderId['id']
    r.calculate_etag()
    query = rinocloud.Query().filter(name=r.name, parent=r._parent).query()

    if len(query) == 0:
        click.echo('File does not exist on Rinocloud. Use `rino notebook push` to create a new notebook on Rinocloud.')
        return

    prev_version = query[0]
    prev_metadata = utils.clean_metadata(prev_version._prep_metadata().copy())

    # merge metadata from prev object
    for key, val in prev_metadata.items():
        r[key] = val

    r.versions = prev_version.versions
    r.versions.append(prev_version.id)

    repo = utils.get_git_repo()

    if repo and repo.is_dirty() and not force:
        click.echo('Refusing to push without --force because git repo is dirty')
        return

    git_metadata = utils.get_git_meta(repo)
    if git_metadata:
        r.git = git_metadata

    new_metadata = utils.clean_metadata(r._prep_metadata().copy())
    if r.etag == prev_version.etag and new_metadata == prev_metadata and not force:
        click.echo('Nothing to update. Old and new versions have the same file hashs and metadata. Not updating without --force.')
        return

    click.echo('Updating %s at %s' % (path, remote))
    delete_rinocloud_object(prev_version.id)

    utils.save_notebook_meta(path, r)
    r.upload()


def fetch(path, force):
    remote = config.get('remote')

    if not remote:
        click.echo('Remote not set. Use `rino remote set <rinocloud_path>` to set the target directory.')
        return

    token = login.get_token()
    rinocloud.api_key = token
    rinocloud.set_local_path(os.getcwd())

    r = rinocloud.Object()
    r.set_name(path, overwrite=True)

    rinoFolderId = utils.get_rino_folder(rinocloud, remote).json()
    r._parent = rinoFolderId['id']

    query = rinocloud.Query().filter(name=r.name, parent=r._parent).query()

    if len(query) == 0:
        click.echo('No file %s/%s exists on Rinocloud' % (remote, path))
        return

    target = query[0]
    target.get()
    utils.save_notebook_meta(path, target)
    target.download()

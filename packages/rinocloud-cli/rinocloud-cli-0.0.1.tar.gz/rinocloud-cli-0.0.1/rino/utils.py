from git import Repo
from git.exc import InvalidGitRepositoryError
import os
import json
import click
import requests


def get_rino_folder(rinocloud, path):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }
    try:
        return requests.post(rinocloud.api_base + 'files/create_folder_if_not_exist/', json={
            'name': path
        }, headers=headers)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError("Could not connect to specified domain %s" % rinocloud.api_domain)


def clean_metadata(meta):
    obj = {}
    for key, val in meta.items():
        if key not in ["id", "created_on", "updated_on", "etag", "filepath", "name", "versions"]:
            obj[key] = val

    return obj


def get_git_repo():
    try:
        repo = Repo(os.getcwd())
        repo.config_reader()
    except InvalidGitRepositoryError as e:
        repo = None
    return repo


def get_git_meta(repo):
    git_metadata = None
    if repo:
        try:
            git_remote = repo.remote()
            git_metadata = {
                'remote_name': git_remote.name,
                'remote_urls': list(git_remote.urls),
                'branch': repo.active_branch.name,
                'commit': repo.head.commit.hexsha
            }
        except ValueError as e:
            click.echo('Cant add git informatoin. git has no remote set.')
    return git_metadata


def make_hidden_json_file(path):
    dirname = os.path.dirname(path)
    fname = os.path.basename(path)

    index_of_dot = fname.index('.')
    fname_no_ext = fname[:index_of_dot]

    return os.path.join(
        dirname,
        '.' + fname_no_ext  + '.json'
    )


def save_notebook_meta(path, obj):
    m = obj._prep_metadata()
    mfile = open(make_hidden_json_file(path), 'w')
    mfile.write(json.dumps(m, indent=4, sort_keys=True))
    mfile.close()


def get_notebook_meta(path):
    mfile_path = make_hidden_json_file(path)
    if not os.path.isfile(mfile_path):
        return None, None
    mfile = open(mfile_path, 'r')
    metadata = json.loads(mfile.read())
    mfile.close()
    return metadata, mfile_path

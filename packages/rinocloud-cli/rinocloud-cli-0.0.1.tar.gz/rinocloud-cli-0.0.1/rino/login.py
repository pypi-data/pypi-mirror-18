import click
import rinocloud
import requests
import keyring


def get_token():
    return keyring.get_password('rinocloud-python-cli', 'token')


def get_email():
    return keyring.get_password('rinocloud-python-cli', 'email')


def get_project():
    return keyring.get_password('rinocloud-python-cli', 'project')


def get_username():
    return keyring.get_password('rinocloud-python-cli', 'username')


def login(email, password):
    url = rinocloud.api_domain + '/o/token/'
    data = {
        'username': email,
        'password': password,
        'grant_type': 'password',
        'client_id': 'XIkmGK9ehXrL0At1MzADGuWcA6V7wFqtwYs7FjM7'
    }

    oauth_r = requests.post(url, data)

    if oauth_r.status_code > 400:
        click.echo(oauth_r.json()['error_description'], err=True, color='red')

    else:
        url = rinocloud.api_base + 'users/details/'
        access_token = oauth_r.json()['access_token']

        headers = {
            'Authorization': 'Bearer %s' % access_token
        }

        r = requests.post(url, headers=headers)

        if r.status_code > 400:
            click.echo(r.json()['error_description'], err=True, color='red')

        else:
            keyring.set_password('rinocloud-python-cli', 'token', r.json()['token'])
            keyring.set_password('rinocloud-python-cli', 'email', email)
            keyring.set_password('rinocloud-python-cli', 'username', r.json()['username'])
            keyring.set_password('rinocloud-python-cli', 'project', r.json()['project'])
            click.echo('Logged in.')


def list():
    token = keyring.get_password('rinocloud-python-cli', 'token')
    email = keyring.get_password('rinocloud-python-cli', 'email')

    click.echo('Logged into Rinocloud as %s' % email)


def logout():
    keyring.delete_password('rinocloud-python-cli', 'token')
    keyring.delete_password('rinocloud-python-cli', 'email')
    keyring.delete_password('rinocloud-python-cli', 'username')
    keyring.delete_password('rinocloud-python-cli', 'project')
    click.echo('Logged out of Rinocloud')

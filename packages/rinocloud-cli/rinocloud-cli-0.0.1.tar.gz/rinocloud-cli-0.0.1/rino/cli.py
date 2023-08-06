import click
import rino

# base cli group
@click.group()
def cli():
    pass

# init
@cli.command()
def init():
    """
        Initializes a rino repo.
    """
    rino.initialize.initialize()

# browse
@cli.command()
def browse():
    """
        Opens your Rinocloud in a webbrowser.
    """
    rino.browse.open()

# user sub group
@cli.group()
def user():
    """
        User commands login/logout.
    """
    pass


### user login
@user.command()
@click.option('--email', prompt='Your Rinocloud login email')
@click.option('--password', prompt='Your Rinocloud password [hidden]', hide_input=True)
def login(email, password):
    """
        Logs you into Rinocloud.
    """
    rino.login.login(email, password)


### user logout
@user.command()
def logout():
    """
        Logs you out of Rinocloud.
    """
    rino.login.logout()

### user list
@user.command()
def list():
    """
        Lists the logged in user
    """
    rino.login.list()

# login command (shortcut to user login)
@cli.command()
@click.option('--email', prompt='Your Rinocloud login email')
@click.option('--password', prompt='Your Rinocloud password [hidden]', hide_input=True)
def login(email, password):
    """
        Logs you into Rinocloud.
    """
    rino.login.login(email, password)

# remote group
@cli.group()
def remote():
    """
        Set/unset target path on Rinocloud.
    """
    pass

### remote set
@remote.command()
@click.argument('path', type=click.Path())
def set(path):
    """
        Set the remote target Rinocloud path.
    """
    rino.remote.set(path)

### remote unset
@remote.command()
def unset():
    """
        Unset the remote target Rinocloud path.
    """
    rino.remote.unset()

### remote list
@remote.command()
def list():
    """
        List the remote target Rinocloud path.
    """
    rino.remote.list()

# notebook group
@cli.group()
def notebook():
    """
        Commands for pushing/fetching notebooks.
    """
    pass

### notebook push
@notebook.command()
@click.argument('file', type=click.Path())
@click.option('--force', is_flag=True)
def push(file, force):
    """
        Push a notebook.
    """
    rino.notebook.push(file, force)

### notebook update
@notebook.command()
@click.argument('file', type=click.Path())
@click.option('--force', is_flag=True)
def update(file, force):
    """
        Update a notebook.
    """
    rino.notebook.update(file, force)

### notebook fetch
@notebook.command()
@click.argument('file', type=click.Path())
@click.option('--force', is_flag=True)
def fetch(file, force):
    """
        Fetch a notebook.
    """
    rino.notebook.fetch(file, force)

# notebook group
@cli.group()
def git():
    """
        Commands for using git with rino.
    """
    pass

# notebook group
@git.command()
@click.argument('file', type=click.Path())
def show(file):
    """
        Show the git commit for the notebook.
    """
    rino.git.show(file)

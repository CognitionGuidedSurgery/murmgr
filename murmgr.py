__author__ = 'Alexander Weigl'

import os
import urllib
import sys
import subprocess
import colorama
import click
import yaml
from path import path

colorama.init()

REPO_LAYOUT_VERSION_SUPPORTED = 1

EMPTY_USER_PACKAGE = "https://github.com/CognitionGuidedSurgery/mup-empty.git"
"URL to the git repository, to create empty packages"

REPOSITORY_TEMPLATE = "https://gist.githubusercontent.com/areku/e4d587de7bc8588f151a/raw/"
"template for MSML_REPO_CONFIG"

MSML_REPO_CONFIG = "msml-repo.yaml"
"name of the msml repository file"

MSML_PACKAGE_CONFIG = "msml-package.yaml"
""

import yaml.representer
yaml.add_representer(path, yaml.representer.SafeRepresenter.represent_unicode)

class AppConfig(object):
    def __init__(self):
        self.verbosity = 0
        self.repository = None
        self.always_yes = False

    def in_repository(self):
        if not self.repository:
            p = path(".") / MSML_REPO_CONFIG
            if p.exists():
                self.repository = path(".").abspath()
        return self.repository and self.repository.exists()


appconfig = AppConfig()
"""Global application config"""


# region santa's helper

class NotInRepositoryError(BaseException): pass


def execute(command, **kwargs):
    cmd = command.format(**kwargs)
    do(cmd)
    retcode = subprocess.call(cmd, stdout=sys.stdout, stderr=sys.stderr, shell=True, cwd=os.getcwd())
    if retcode > 0:
        error("Could not execute: %s" % cmd)


def read_yaml(filename):
    with file(filename) as fp:
        return yaml.safe_load(fp.read())

def store_yaml(obj, filename):
    import StringIO

    try: # safety first, do not open file before we can safely dump
        s = StringIO.StringIO()

        yaml.dump(obj, s)

        with file(filename, 'w') as fp:
            fp.write(s.getvalue())
    except IOError:
        raise


def get_repo_config(repository = None, filename = None):
    if repository and not filename:
        filename = repository / MSML_REPO_CONFIG
    elif appconfig.in_repository() and not filename:
        filename = appconfig.repository / MSML_REPO_CONFIG

    if not filename:
        raise NotInRepositoryError()

    config = read_yaml(filename)

    if int(config['repo_layout_version']) != REPO_LAYOUT_VERSION_SUPPORTED:
        error("Repository layout version is not %d" % REPO_LAYOUT_VERSION_SUPPORTED)
        sys.exit(1)

    return config

def save_repo_config(config, repository=None, filename=None):
    assert config

    if repository and not filename:
        filename = repository / MSML_REPO_CONFIG
    elif appconfig.in_repository():
        filename = appconfig.repository / MSML_REPO_CONFIG

    store_yaml(config, filename)


def error(message):
    click.echo(click.style("ERROR: ", fg='red') + message, err=True)


def warning(message):
    click.echo(click.style("WARNING: ", fg='yellow') + message, err=True)


def do(message):
    click.echo(click.style(">>> ", fg='blue') + message, err=False)

def go_into_repository():
    if appconfig.in_repository():
        os.chdir(appconfig.repository)
    else:
        raise NotInRepositoryError

def get_package_config(name=None, folder=None):
    def prefix_paths(prefix, seq):
        return map(lambda x: (prefix / x).abspath(), seq)

    def prefix_paths_inplace(config, key):
        config[key] = prefix_paths(folder.abspath(), config.get(key, []))

    if name:
        folder = appconfig.repository / name

    if not folder:
        raise BaseException("Not valid package folder given.")


    config = read_yaml(filename=folder / MSML_PACKAGE_CONFIG)

    config['folder'] = folder.abspath()

    prefix_paths_inplace(config, 'alphabet-directories')
    prefix_paths_inplace(config, 'binary-search-path')
    prefix_paths_inplace(config, 'python-path')

    return config


def get_packages():
    try:
        config = get_repo_config()
        packages = config.get('packages', [])

        for p in packages:
            yield get_package_config(p)


    except NotInRepositoryError:
        error("Not in a repository")
# endregion

def ask_yes_no(prompt, default = True):
    if appconfig.always_yes:
        return default
    else:
        d = "Yn" if default else "yN"
        val = click.prompt(prompt+" [%s]" % d)

        if val in ('y', 'Y'):
            return True
        elif val in ('n','N'):
            return False
        else:
            return default

@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-r", "--repository", help="give a path to an repository", type=path)
@click.option("-y", "--always-yes/--always-no", default=False)
def cli(verbose=0, repository=None, always_yes = False):
    appconfig.verbosity = verbose
    appconfig.always_yes = always_yes
    if repository:
        appconfig.repository = path(repository).abspath()
    else:
        try:
            appconfig.repository = path(os.environ['MSML_REPOSITORY']).abspath()
        except KeyError:
            appconfig.repository = None

@click.command()
@click.argument("name")
@click.pass_context
def new_package(ctx, name):
    """creates a new user package.

    """


    p = path(name).abspath()
    curdir = path(".").abspath()

    try:
        os.mkdir(p)
        os.chdir(p)
        execute("git init")
        execute("git remote add base {repo}", repo=EMPTY_USER_PACKAGE)
        execute("git pull base master")

        os.chdir(curdir)

        if appconfig.in_repository():
            if ask_yes_no("Activate user package %s" % name):
                ctx.invoke(activate_package, filepath=p)
    except OSError:
        click.echo(click.style("Folder '%s' already exists!" % name, fg='red'), err=True)


@click.command()
@click.argument("filepath")
def activate_package(filepath):
    config = get_repo_config()
    fp = path(filepath).relpath(appconfig.repository)

    if not fp.exists():
        warning("The folder '%s' does not exists!")

    l = config.get('packages', list())
    if l is None:
        l = list()
    try:
        if fp not in l:  # no duplicates
            l.append(str(fp))
        else:
            warning("%s already in the list of active packages" % filepath)
    except AttributeError:  # not a list
        l = [fp]

    config['packages'] = l

    save_repo_config(config)


@click.command()
@click.argument("filepath")
def deactivate_package(filepath):
    config = get_repo_config()

    fp = filepath.abspath()

    l = config.get('packages', list())


    try:
        config['packages'] = filter(
            lambda x: path(x).abspath() != fp, l
        )
    except TypeError:
        error("Wrong data type detected!")
        raise

    save_repo_config(config)


@click.command()
@click.argument("name")
def new_repository(name):
    try:
        os.mkdir(name)
        os.chdir(name)
        do("Create git repository")
        execute("git init")
        do("Downloading configuration template")
        urllib.urlretrieve(REPOSITORY_TEMPLATE, MSML_REPO_CONFIG)
    except OSError:
        error("Folder '%s' already exists!" % name)

@click.command()
@click.argument("url")
@click.option("-n", "--name")
@click.pass_context
def download_package(ctx, url, name = None):
    """
    """

    if not name:
        import re
        pattern = re.compile(r"(.+)/(?P<name>.+?).git")
        name = str(pattern.search(url).group('name'))

    try:
        go_into_repository()
        do("Enable submodule %s" % name)
        execute("git submodule add {repo} {name}" , repo = url, name = name)
        ctx.invoke(activate_package, filepath = path('.')/name)
    except NotInRepositoryError:
        error("Not in a msml repository")

@click.command()
def update_repository():
    try:
        go_into_repository()
        execute("git submodule foreach git pull origin master")
    except NotInRepositoryError:
        error("Not in a msml repository")





@click.command()
def show():
    def echo_filepaths(category, seq):
        click.echo(click.style(category, fg='blue'))
        rep = len(appconfig.repository.abspath())-1
        for p in seq:
            click.echo(
                "\t"+
                click.style(p[:rep], fg='yellow')
                +click.style(p[rep:], fg='yellow', bold=True)
            )

    if appconfig.in_repository():
        config = get_repo_config()

        alphabet_dirs = []
        bin_dirs = []
        py_dirs = []

        for package in get_packages():
            py_dirs += package.get('python-path', [])
            bin_dirs += package.get('binary-search-path', [])
            alphabet_dirs += package.get('alphabet-directories', [])

            click.echo(
                click.style(package['name'],fg='blue')
                +click.style('@',fg='yellow')
                +click.style(package['version'],fg='red')
                +"\tin " + package['folder']
            )

        echo_filepaths("Alphabet", alphabet_dirs)
        echo_filepaths("Binary", bin_dirs)
        echo_filepaths("Python", py_dirs)

        if appconfig.verbosity > 1:
            import pprint

            click.echo("Repository Config:")
            pprint.pprint(config)
    else:
        error("Not in a repository!")


cli.add_command(new_package)
cli.add_command(new_repository)
cli.add_command(show)
cli.add_command(activate_package)
cli.add_command(deactivate_package)
cli.add_command(update_repository)
cli.add_command(download_package)

if __name__ == "__main__":
    cli()
import os
from fabric.contrib.files import append
from fabric.decorators import task
from fabric.operations import local, run, put
from fabric.context_managers import settings, lcd
from fabric.state import env
from fabric.tasks import execute
from context_managers import bash
from yurt import main
from utils import recursive_file_modify, add_fab_path_to_bashrc, get_fab_settings, \
    generate_printable_string, generate_ssh_keypair, get_environment_pem, get_project_name_from_repo

__author__ = 'deanmercado'

###
# fab setup commands: these commands setup a new django project
###


# @task
@main.command()
def create_project():
    """
    Creates Django project by copying over
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))
    env.settings['project_name'] = env.proj_name
    local("cp -rf ./yurt_core/../django_project/ ./{0}".format(env.proj_name))
    recursive_file_modify(os.path.abspath("./{0}".format(env.proj_name)), env.settings)


@main.command()
def load_orchestration_and_requirements():
    """
    Copies over the orchestration directory and requirements.txt file to current directory
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))
    env.repo_name = get_project_name_from_repo(env.settings.get('git_repo'), False)
    env.settings['project_name'] = env.proj_name
    env.settings['repo_name'] = env.proj_name

    local('cp -rf ./yurt_core/../orchestration ./{0}'.format(env.proj_name))
    local('cp -f ./yurt_core/requirements.txt ./{0}'.format(env.proj_name))
    recursive_file_modify('./{0}/orchestration'.format(env.proj_name), env.settings)


@main.command()
def enable_git_repo():
    """
    Sets up git repository in project direcory
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))

    if env.proj_name not in os.listdir('.'):
        local('mkdir {0}'.format(env.proj_name))

    with lcd(env.proj_name):
        with settings(warn_only=True):
            local('git init')
            local('git remote add origin {0}'.format(env.git_repo_url))
            local('git checkout -b develop')


@main.command()
def move_vagrantfile_to_project_dir():
    """
    Moves Vagrantfile from `orchestration` directory to project directory
    :return:
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))
    local('mv ./{0}/orchestration/Vagrantfile .'.format(env.proj_name))


@main.command()
def create_pem_file():
    """
    Generates an SSH Key Pair (that is added to your keychain and `~/.ssh` directory)
    :return:
    """
    pub, pem = generate_ssh_keypair(in_template=False)

    project_name = raw_input("What will you name this ssh_key?\
    (Hint: just an alphanumeric name that describes what the key is for):\t")

    with open("./{0}.pem".format(project_name), 'w') as key:
        key.write(pem)
        os.chmod("./{0}.pem".format(project_name), 0400)
        local("mv ./{0}.pem ~/.ssh".format(project_name))
    with open("./{0}.pub".format(project_name), 'w') as key:
        key.write(pub)
        local("mv ./{0}.pub ~/.ssh".format(project_name))
        local("ssh-add ~/.ssh/{0}.pem".format(project_name))
    print("PEM-file `~/.ssh/{0}.pem` added!".format(project_name))


@main.command()
def copy_pem_file(user=None, host=None, key_name=None):
    """
    Appends public SSH Key (named after `project_name` in `fabric_settings.py`) to remote host
    :param user: str, Remote user
    :param host: str, Remote ip address
    :param key_name: str, Name of Key_pair in ~/.ssh
    :return:
    """
    project_name = key_name
    env.user = user
    env.host_string = host

    if user is None:
        user = raw_input("SSH User? (default: 'root'):\t")
        if user.strip(" ") == "":
            env.user = "root"
        else:
            env.user = user
    if host is None:
        env.host_string = raw_input("Public IP/DNS of Remote Server?:\t")
    if key_name is None:
        KEYNAME_ENUM = {}
        key_names = set([filename.split('.')[0]
                         if "." in filename
                         else filename
                         for filename in os.listdir(os.path.expanduser("~/.ssh"))])
        key_names.remove("config")
        print("Option\tKeyname")
        print("______\t_______")
        for index, keyname in enumerate(key_names):
            KEYNAME_ENUM[str(index)] = keyname
            print("{0}:\t{1}".format(index, keyname))
        print("")
        try:
            project_name = KEYNAME_ENUM[raw_input("".join(("Which key in ~/.ssh are you ",
                                                           "copying to the remote server (Input the option)?:\t")))]
        except KeyError:
            raise KeyError("Not a good input!")
            return
    print("If prompted for 'Passphrase for private key:', input the password credentials for this server.")
    run('mkdir -p ~/.ssh')
    with open(os.path.expanduser('~/.ssh/{0}.pub'.format(project_name)), 'r') as key:
        append("~/.ssh/authorized_keys", key.readline().rstrip("\n"))
    if env.user == "root":
        print("Pub key added to `/{0}/.ssh/authorized_keys` in server".format(env.user))
    else:
        print("Pub key added to `/home/{0}/.ssh/authorized_keys` in server".format(env.user))


@main.command()
def delete_fabric_settings():
    """
    Deletes `fabric_settings.py`
    :return: None
    """
    backup_fab_settings = raw_input("Backup `fabric_settings.py` before it's deleted (Y/N)?")
    if backup_fab_settings.lower() == 'y':
        print('Backing up `fabric_settings.py` => `fabric_settings.py.bak`')
        local('cp fabric_settings.py fabric_settings.py.bak')
    elif backup_fab_settings.lower() == 'n':
        print('No backup made!')
    else:
        print('Bad input. Re-run by calling `fab setup.delete_fabric_settings`')
        return None
    print('Deleting `fabric_settings`')
    local('rm fabric_settings.py')
    local('rm *.pyc')


@main.command()
def new(PEM_copy=None):
    """
    Create new project
    :return: Void
    """
    env.settings = get_fab_settings()
    env.proj_name = get_project_name_from_repo(env.settings.get('git_repo'))
    env.settings['project_name'] = env.proj_name
    env.git_repo_url = env.settings.get('git_repo')
    execute(enable_git_repo)
    execute(create_project)
    execute(load_orchestration_and_requirements)
    execute(move_vagrantfile_to_project_dir)
    if PEM_copy:
        execute(create_pem_file)
        environment = get_environment_pem(message='Export PEM file to remote')
        execute(copy_pem_file, environment=environment)
    delete_choice = {
        'y': True,
        'n': False
    }
    local('vagrant up')
    try:
        delete_setting = delete_choice[raw_input('''Delete `fabric_settings.py` file (Y/N)?
Hint: If you plan on running more fab calls after this, enter `N`.\nChoice:\t''').lower()]
    except KeyError:
        print("Bad input. `fabric_settings.py` not deleted.")
        return None

    if delete_setting:
        execute(delete_fabric_settings)


@main.command()
def existing():
    """
    Sets up existing project local environment
    :return:
    """
    git_repo = raw_input("Enter the git repository link\n(i.e. git@github.com:mr_programmer/robot_repository.git):\t")
    project_name = get_project_name_from_repo(git_repo)
    repo_name = get_project_name_from_repo(git_repo, False)
    env.settings = {
        'git_repo': git_repo,
        'project_name': project_name
    }
    local("git clone {0}".format(git_repo))
    local("mv ./{0} ./{1}".format(repo_name, project_name))
    local("cp ./yurt_core/../orchestration/Vagrantfile ./")
    recursive_file_modify('./Vagrantfile', env.settings, is_dir=False)
    local("vagrant up")


@main.command()
def add_settings():
    """
    Adds `fabric_settings.py` to this directory
    """
    public_key, private_key = generate_ssh_keypair()
    SETTINGS = {
        'git_public_key': public_key,
        'git_private_key': private_key,
        'vagrant': {
            'db_pw': generate_printable_string(15, False),
            'secret_key': generate_printable_string(40)
        }
    }
    if 'fabric_settings.py' in os.listdir('.'):
        continue_process = raw_input('You already have `fabric_settings.py in this folder. Overwrite? (Y/N)')
        if continue_process.lower() == 'y':
            pass
        else:
            print("Aborted.")
            return False
    local('cp ./yurt_core/fabric_settings.py.default.py ./fabric_settings.py')
    recursive_file_modify('./fabric_settings.py', SETTINGS, is_dir=False)
    print("".join(("You now have `fabric_settings.py`. Edit this file to have the correct ",
                   "values and then enter `fab setup.new`")))

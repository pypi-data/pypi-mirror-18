# coding:utf-8
import json
import sys
import django
import platform
import pip
import pipdeptree
from django.http import HttpResponse, Http404
from django.db import connection
from django.conf import settings


def get_virtualenv_packages():
    """
    Return list of installed packages in the virtualenv of application
    """
    activate_this_file = "/var/www/vhosts/" + settings.SYSTEM_INFORMATION_APPLICATION_NAME
    activate_this_file += ".epfl.ch/private/" + settings.SYSTEM_INFORMATION_APPLICATION_NAME + "-env/bin/activate_this.py"
    execfile(activate_this_file, dict(__file__=activate_this_file))
    return sorted(["%s==%s" % (i.key, i.version) for i in pip.get_installed_distributions()])

def get_requirement_packages():
    """
    Return list of requirements packages
    Each package can have some dependences
    """
    packages = []

    # TODO 1: Il faut pouvoir spécifier le requirement de production
    #         et pas seulement le _base.txt
    # TODO 2: Offrir une constante SYSTEM_INFORMATION_REQUIREMENT_BASE_FILE
    #         permettant à l'utilisateur d'indiquer son requirement
    fname = settings.BASE_DIR.child("requirements").child("_base.txt")

    with open(fname) as f:
        for line in f:
            packages.append(line.split("\n")[0])
        return packages

def get_virtual_dependencies_of_packages():
    """
    Return information about installed dependencies in the virtualenv of application

    example of json result :

    {"dependencies": [{"required_version": null,
        "installed_version": "1.8.13", "package_name": "Django", "key": "django"}],
    "package_name": "django-ckeditor"}
    """
    packages = pip.get_installed_distributions()
    dist_index = pipdeptree.build_dist_index(packages)
    tree = pipdeptree.construct_tree(dist_index)

    return [{'package_name': k.as_dict()['key'], 'dependencies': [v.as_dict() for v in vs]}
            for k, vs in tree.items()]

def get_django_version():
    """
    Return the version of Django
    """
    return django.__version__

def get_python_version():
    """
    Return the version of python
    """
    return ".".join(map(str, sys.version_info[:3]))

def get_database_version():
    """
    Return the version of database
    """
    cursor = connection.cursor()
    cursor.execute("SELECT VERSION();")
    row = cursor.fetchone()
    return row[0]

def get_os_version():
    """
    Return the version of OS
    """
    return platform.platform()

def get_information(request):
    """
    Return information about the application
    """
    client_ip = request.META['REMOTE_ADDR']
    
    if not request.user.is_superuser and client_ip != '128.178.109.61':
        data = json.dumps("You don't have permission")
    else:
        information_dict = {}
        information_dict['service_name'] = settings.SYSTEM_INFORMATION_APPLICATION_NAME
        information_dict['django_version'] = get_django_version()
        information_dict['python_version'] = get_python_version()
        information_dict['db_version'] = get_database_version()
        information_dict['os_version'] = get_os_version()
        information_dict['virtualenv_packages'] = get_virtualenv_packages()
        information_dict['requirement_packages'] = get_requirement_packages()
        information_dict['virtualenv_dependencies'] = get_virtual_dependencies_of_packages()

        data = json.dumps(information_dict)

    return HttpResponse(
        data,
        content_type='application/javascript; charset=utf8'
    )

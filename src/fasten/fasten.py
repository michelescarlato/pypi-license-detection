"""Main module."""
import logging
import requests


def get_pkg_metadata(forge, pkg_name, pkg_version):
    """
    Requests the package metadata from FASTEN's RESTAPI

    Args:
        forge (str): Forge of the package - Default: pypi
        pkg_name (str): Package name
        pkg_version (str): Package version
    """
    logging.debug(f"forge {forge}, pkg name {pkg_name}, pkg version {pkg_version}")
    url = f"https://api.fasten-project.eu/api/{forge}/packages/{pkg_name}/{pkg_version}"
    logging.debug(url)

    res = requests.get(url)

    if res.status_code != 200:
        logging.debug(res.status_code)

    return res.json()


def get_pkg_version(forge, pkg_name):
    """
    Get the latest know version of a given package

    Args:
        forge (str): Package forge
        pkg_name (str): Package name
    """
    version = "1.1"
    # TODO: implement a way to get the latest version of a package from the RESTAPI
    return version

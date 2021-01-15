"""Main module."""
import logging
from typing import Dict

import requests

logger = logging.getLogger(__name__)


def get_pkg_metadata(forge: str, pkg_name: str, pkg_version: str) -> Dict[str, str]:
    """
    Requests the package metadata from FASTEN's RESTAPI

    Args:
        forge (str): Forge of the package - Default: pypi
        pkg_name (str): Package name
        pkg_version (str): Package version
    """
    logger.debug("forge %s, pkg name %s, pkg version %s", forge, pkg_name, pkg_version)
    url = f"https://api.fasten-project.eu/api/{forge}/packages/{pkg_name}/{pkg_version}"
    logger.debug(url)

    res = requests.get(url)

    if res.status_code != 200:
        logger.debug("Request status code: %s", res.status_code)

    return res.json()


def get_pkg_version(forge: str, pkg_name: str) -> str:
    """
    Get the latest know version of a given package

    Args:
        forge (str): Package forge
        pkg_name (str): Package name
    """
    version = "1.1"
    # TODO: implement a way to get the latest version of a package from the RESTAPI
    return version

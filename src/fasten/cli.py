"""Console script for fasten."""
import click
from fasten import fasten
import logging

logger = logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


@click.group()
def cli():
    logging.info("Started")
    logging.info("Finished")


@cli.command()
@click.option(
    "-f",    "--forge",    default="pypi",    type=str,
    help="Forge of the package (pypi, mvn or debian)",
)
@click.option(
    "-v",
    "--version",
    default=None,
    type=str,
    help="Version of the package. By default it looks for the latest version on PyPI.",
)
@click.argument("pkg_name")
def check(forge, version, pkg_name):
    """
    Given a package name, FASTEN will return all metadata.

    Args:
        forge (str): Forge of the package (pypi, mvn or debian) - Default: pypi
        version (str): Package version - Default: latest known version
        pkg_name (str): Package name
    """
    if version is None:
        version = fasten.get_pkg_version(forge, pkg_name)
        logger.debug(f"package version: {version}")
    click.echo(f"Retrieving metadata: {forge}, {pkg_name}, {version}...")
    result = fasten.get_pkg_metadata(forge, pkg_name, version)
    click.echo(f"Result:\n {result}\n")


@cli.command()
def check_all():
    """
    Given the output of `requirements.txt`, FASTEN will return all metadata for each package.
    """

    # get a list from requirements.txt
    pkgs_list = [
        {
            "name": "test_pkg1",
            "version": "version_test_pkg1",
            "forge": "test_pkg_forge1",
        },
        {
            "name": "test_pkg2",
            "version": "version_test_pkg2",
            "forge": "test_pkg_forge2",
        },
    ]

    click.echo(f"Retrieving metadata for the packages: {pkgs_list}")

    result = []
    # for each pkg, run check and return its metadata.
    for pkg in pkgs_list:
        result.append(
            fasten.get_pkg_metadata(pkg["forge"], pkg["name"], pkg["version"])
        )

    click.echo(f"Results: \n{result}\n")

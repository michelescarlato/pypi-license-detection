"""Console script for fasten."""
import sys
import click

@click.group()
def cli():
    pass


@cli.command()
@click.argument('pkg_name')
def check(pkg_name):
    """
    Given a package name, FASTEN will return all metadata.
    (GET to EP4)
    """
    click.echo(f'Retrieving metadata: {pkg_name}')


@cli.command()
@click.argument('pkg_name')
def check_all():
    """
    Given the output of pip list, FASTEN will return all metadata for each 
    package.
    """
    # get a list from pip list or requirements.txt
    # pip_list = pip_int.main(['list'])
    # click.echo(pip_list)
    pkg_list = ['pkg1', 'pkg2']

    click.echo(f'Retrieving metadata for the packages: {pkg_list}')

    # for each pkg, run check and return its metadata.


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover

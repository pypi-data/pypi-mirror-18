import click
import socket
import logging

logging.basicConfig()


@click.command()
@click.option('--name', prompt='Domain name',
              help='The domain you want to query.')
def simple(name):
    """Simple query for domain."""
    logger = logging.getLogger('dns_query')
    logger.warning(simple_impl(name))


def simple_impl(domain):
    """Simple query domain name by using python module."""
    logger = logging.getLogger('dns_query')
    logger.warning("Query domain:" + domain)
    ips = socket.gethostbyname_ex(domain)[2]
    logger.warning(ips)
    return ips


if __name__ == '__main__':
    simple()
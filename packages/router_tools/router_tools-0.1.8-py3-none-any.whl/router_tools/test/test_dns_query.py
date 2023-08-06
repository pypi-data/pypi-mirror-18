import logging
from router_tools import dns_query

logging.basicConfig()


def test_dns_query_simple():
    dns_query.simple_impl("www.baidu.com")
    pass


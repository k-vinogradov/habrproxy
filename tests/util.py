# pylint: disable=missing-docstring

from os.path import abspath, dirname, join

HOSTNAME = "localhost"
PROXY_PORT = 8080
MOCK_PORT = 9000


def get_mock_address():
    return "http://{}:{}".format(HOSTNAME, MOCK_PORT)


def get_proxy_address():
    return "http://{}:{}".format(HOSTNAME, PROXY_PORT)


def get_project_dir():
    return abspath(join(dirname(abspath(__file__)), ".."))


def get_data_dir():
    return join(dirname(abspath(__file__)), "data")


def read_file(filename):
    with open(join(get_data_dir(), filename)) as html:
        return html.read()


def read_original_html():
    return read_file("original.html").replace("ANCHOR_ADDRESS", get_mock_address())


def read_expected_html():
    return read_file("expected.html").replace("ANCHOR_ADDRESS", get_proxy_address())

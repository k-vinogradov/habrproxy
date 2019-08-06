"""Integrated test uses simple mock server and run tested app with subprocess."""

import http.server
import os
import subprocess
import sys
import threading
import time
import urllib.request
import pytest
from tests.util import (
    get_proxy_address,
    get_mock_address,
    read_expected_html,
    read_original_html,
    get_project_dir,
    HOSTNAME,
    MOCK_PORT,
    PROXY_PORT,
)


@pytest.fixture(scope="module")
def mock_address():
    """Run mock web-server in thread."""

    class RequestHandler(http.server.BaseHTTPRequestHandler):
        """Mock server request handler."""

        def redirect_to_page(self):
            """Reply with redirect to the main page."""
            page_url = "{}/page".format(get_mock_address())
            self.send_response(302)
            self.send_header("Location", page_url)
            self.end_headers()

        def send_page(self):
            """Reply with original page content."""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(bytes(read_original_html(), "UTF-8"))

        def do_GET(self):  # pylint: disable=invalid-name
            """Handle GET request."""
            if self.path == "/redirect":
                self.redirect_to_page()
            else:
                self.send_page()

    httpd = http.server.HTTPServer((HOSTNAME, MOCK_PORT), RequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.start()
    yield get_mock_address()
    httpd.shutdown()
    thread.join()


@pytest.fixture(scope="module")
def proxy_address(mock_address):  # pylint: disable=redefined-outer-name
    """Run proxy app in subprocess."""
    python = sys.executable
    working_dir = get_project_dir()
    script = os.path.join(working_dir, "habrproxy", "bin", "run.py")
    args = [python, script, "--remote-address", mock_address, "--port", str(PROXY_PORT)]
    proxy = subprocess.Popen(args, env=dict(os.environ, PYTHONPATH=working_dir))
    time.sleep(0.5)
    yield get_proxy_address()
    proxy.send_signal(2)


def test_full_flow(proxy_address):  # pylint: disable=redefined-outer-name
    """Main test routine."""
    url = "{}/redirect".format(proxy_address)
    response = urllib.request.urlopen(url)
    assert response.read().decode("utf-8") == read_expected_html()

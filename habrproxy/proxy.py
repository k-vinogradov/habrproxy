"""Habrproxy Main Module."""

from logging import getLogger
from aiohttp import web, ClientSession, ClientConnectionError
from habrproxy.parser import build_response_content

LOGGER_NAME = "habrproxy"
OMIT_RES_HEADERS = ["Content-Encoding", "Transfer-Encoding"]
OMIT_REQ_HEADERS = ["Accept-Encoding"]


def filter_headers(http_obj, filtered):
    """Exclude some headers."""
    return {name: val for name, val in http_obj.headers.items() if name not in filtered}


def setup_routes(proxy, remote_address, local_address):
    """Define request handler and configure the router."""

    async def build_response(original_response):
        if original_response.content_type == "text/html":
            origin_content = (await original_response.content.read()).decode()
            body = build_response_content(origin_content, remote_address, local_address)
        else:
            body = await original_response.content.read()
        headers = filter_headers(original_response, OMIT_RES_HEADERS)
        if "Location" in headers:
            location = headers["Location"]
            headers["Location"] = location.replace(remote_address, local_address)
        return web.Response(body=body, status=original_response.status, headers=headers)

    async def handle_request(client_request):
        headers = filter_headers(client_request, OMIT_REQ_HEADERS)
        headers["Host"] = hostname
        request = {
            "method": client_request.method,
            "url": "{}{}".format(remote_address, client_request.rel_url),
            "headers": headers,
            "allow_redirects": False,
            "data": await client_request.read(),
        }
        async with ClientSession() as session:
            try:
                async with session.request(**request) as response:
                    logger.debug(
                        "%s : %s -> %d, %s",
                        request["method"],
                        request["url"],
                        response.status,
                        response.content_type,
                    )
                    return await build_response(response)
            except ClientConnectionError as exc:
                msg = "{} : {} -> {}".format(
                    request["method"], request["url"], str(exc)
                )
                logger.error(msg)
                return web.HTTPBadGateway(reason=msg)

    logger = getLogger(LOGGER_NAME)
    _, hostname = remote_address.split("://", 1)
    proxy.router.add_route("*", "/{tail:.*}", handle_request)


def app(remote_address, local_port):
    """Main application routine."""
    local_address = "http://localhost:{}".format(local_port)
    proxy = web.Application()
    setup_routes(proxy, remote_address, local_address)
    logger = getLogger(LOGGER_NAME)
    logger.info("Run habrproxy...")
    logger.info(
        "To see modified %s content open %s in your browser",
        remote_address,
        local_address,
    )
    web.run_app(proxy, port=local_port)
    logger.info("Exit habrproxy")

"""HTML parser and response text content generator."""
import logging
import re
from html.parser import HTMLParser
from favink import FiniteAutomata, InvalidTransition

REGEXP = r"(?<=\b)[\w]{6}(?=\b)"


def get_text_handler(regexp, postfix):
    """Get function to add postfix for every regexp matched substring."""

    def handler(data):
        if not data.strip():
            return data
        return regexp.sub(lambda m: m.group(0) + postfix, data)

    return handler


class TextContentModifier(HTMLParser, FiniteAutomata):
    """Response contetnt builder."""

    transitions = {
        "start": ["init", "enabled"],
        "enable": ["disabled", "enabled"],
        "disable": [("enabled", "disabled"), "disabled"],
        "stop": [("enabled", "disabled"), "complete"],
    }

    def __init__(self, remote_addr, local_addr, reg_exp, postfix, *args, **kwargs):
        HTMLParser.__init__(self, *args, **kwargs)
        FiniteAutomata.__init__(self)
        self.response_content = []
        self.data_handler = lambda s: s
        self.deep_count = 0
        self.remote_address = remote_addr
        self.local_address = local_addr
        self.regexp = re.compile(reg_exp)
        self.postfix = postfix

    def get_response_content(self):
        """Get the response content string."""
        return "".join(self.response_content)

    # pylint: disable=missing-docstring
    def on_enabled(self, *_):
        self.data_handler = get_text_handler(self.regexp, self.postfix)

    def on_disabled(self, *_):
        self.data_handler = lambda s: s

    def on_complete(self, *_):
        self.data_handler = lambda s: s

    # pylint: enable=missing-docstring

    def error(self, message):
        from habrproxy.proxy import LOGGER_NAME

        logging.getLogger(LOGGER_NAME).error("Parser error: %s", message)

    def handle_data(self, data):
        self.response_content.append(self.data_handler(data))

    def handle_decl(self, decl):
        self.response_content.append("<!{}>".format(decl))

    def handle_startendtag(self, tag, attrs):
        self.response_content.append(self.get_starttag_text())

    def handle_starttag(self, tag, attrs):
        def format_attribute(attr):
            name, value = attr
            if name == "href":
                value = value.replace(self.remote_address, self.local_address)
            return '{}="{}"'.format(name, value)

        def handle_anchor():
            attributes_string = " ".join(map(format_attribute, attrs))
            return "<a {}>".format(attributes_string)

        def handle_body():
            self.start()  # pylint: disable=no-member
            return self.get_starttag_text()

        def handle_disabled_tag():
            try:
                self.disable()  # pylint: disable=no-member
                self.deep_count += 1
            except InvalidTransition:
                pass
            return self.get_starttag_text()

        handlers_map = {
            "a": handle_anchor,
            "body": handle_body,
            "script": handle_disabled_tag,
        }
        try:
            self.response_content.append(handlers_map[tag]())
        except KeyError:
            self.response_content.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        def handle_disabled_tag():
            if self.get_state() != "disabled":
                return
            self.deep_count -= 1
            if self.deep_count == 0:
                self.enable()  # pylint: disable=no-member

        def handle_body():
            self.stop()  # pylint: disable=no-member

        handlers_map = {"body": handle_body, "script": handle_disabled_tag}
        try:
            handlers_map[tag]()
        except KeyError:
            pass
        self.response_content.append("</{}>".format(tag))


def build_response_content(original_content, remote_address, local_address):
    """Build the response content string by parsing the original HTML."""
    parser = TextContentModifier(remote_address, local_address, REGEXP, "&trade;")
    parser.feed(original_content)
    return parser.get_response_content()

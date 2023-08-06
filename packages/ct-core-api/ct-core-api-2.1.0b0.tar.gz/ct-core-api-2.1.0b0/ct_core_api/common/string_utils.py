import re

import HTMLParser
import bleach
from markupsafe import Markup


DEFAULT_ALLOWED_HTML_TAGS = [
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'br',
    'code',
    'div',
    'em',
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'i',
    'li',
    'ol',
    'p',
    'span',
    'strong',
    'ul',
]

DEFAULT_ALLOWED_HTML_ATTRS = {
    'a': ['href', 'title', 'target'],
    'abbr': ['title'],
    'acronym': ['title'],
}


# TODO: Incorporate lxml enhancements from main-app
def clean_html(value, default='', escape=False, markup=True, allowed_tags=None, allowed_attrs=None):
    """Remove evil html tags, returns markup html."""
    if not value:
        return default
    if allowed_tags is None:
        allowed_tags = DEFAULT_ALLOWED_HTML_TAGS
    if allowed_attrs is None:
        allowed_attrs = DEFAULT_ALLOWED_HTML_ATTRS
    # strip removes it, if false it would escape
    r = bleach.clean(value, tags=allowed_tags, attributes=allowed_attrs, strip_comments=True, strip=not escape)

    # Fix escaping issue: https://github.com/jsocol/bleach/issues/143
    entity_replacements = {
        '\xa0': '&nbsp;'
    }

    def swap_entities(text):
        for k, v in entity_replacements.items():
            text = re.sub(k, v, text)
        return text

    r = swap_entities(r)

    return Markup(r) if markup else r


def tokenize(s, *delimiters):
    """Return a list of the tokens in the string s by partitioning on the provided delimiters."""
    return filter(None, re.split(r"({})".format('|'.join([re.escape(x) for x in delimiters])), s))


_html_parser = HTMLParser.HTMLParser()


def unescape_entities(value):
    if value is None:
        return
    return _html_parser.unescape(value)


def camel_to_snake(value):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_spinal(value, screaming=False):
    return getattr(value.replace('_', '-'), 'upper' if screaming else 'lower')()


def spinal_to_snake(value, screaming=False):
    return getattr(value.replace('-', '_'), 'upper' if screaming else 'lower')()


def strip_sensitive_data_from_multidict(multidict):
    """
    Creates a new MultiDict with sensitive data blotted out for logging purposes.  Tightly coupled to the Flask
    logger and werkzeug.datastructures classes, we might want to make this more generic in the future.
    :param multidict: Multidict
    :return: Dictionary of keys and values (potentially stripped)
    """
    from werkzeug.datastructures import MultiDict

    # A bit overkill for now, since we have so few exceptions, and I'd hate for something to actually sneak through
    sensitive_regex = [
        r'.*account.*',
        r'.*bank.*',
        r'.*password.*',
        r'.*routing.*'
    ]

    stripped_multidict = MultiDict()

    # We perform an iterlists so that we get duplicates of the same key.
    for key, value in multidict.iterlists():
        for regex in sensitive_regex:
            match = re.match(regex, key, re.DOTALL | re.IGNORECASE)
            if match:
                value = u'************'
                break

        stripped_multidict.add(key, value)

    return stripped_multidict

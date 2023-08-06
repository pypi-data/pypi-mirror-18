# -*- coding: utf-8 -*-

import os
import re

LOGBOOK_DIRECTORY = '.blogbook'

CONTENT_DIRECTORY = 'content'
FILENAME_REGEX = re.compile('^((\d{4})-(\d{2})-(\d{2})-)?(.*)\.md$', re.IGNORECASE)
MARKDOWN_EXT = '.md'

BUILTIN_LAYOUT_PATH = os.path.join(os.path.dirname(__file__), 'layouts')
LAYOUTS_DIRECTORY = '_layout'
LAYOUT_EXT = '.html'
ASSETS_DIRECTORY = 'assets'

URL_SEPARATOR = '/'

SSH_HOST_KEYS = os.path.expanduser('~/.ssh/known_hosts')

DEFAULT_OUTPUT = '_html'

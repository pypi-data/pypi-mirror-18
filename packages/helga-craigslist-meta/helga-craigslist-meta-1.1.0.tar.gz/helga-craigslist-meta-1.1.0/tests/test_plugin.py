import sys
try:
    from unittest import mock
except ImportError:
    from mock import mock
# kinda nasty hack since helga doesnt support py3 :(
sys.modules['helga.plugins'] = mock.Mock()
from helga_craigslist_meta import plugin

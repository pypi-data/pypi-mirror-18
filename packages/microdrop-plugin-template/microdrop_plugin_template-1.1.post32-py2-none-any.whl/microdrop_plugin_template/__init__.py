'''
Replace with customized contents of `__init__.py.template`.
'''
from datetime import datetime
import sys
import textwrap

from pip_helpers import install


def install_requirements(plugin_root, ostream=sys.stdout):
    print >> ostream, ('[%s] Processing post-install hook for: %s' %
                       (str(datetime.now()), plugin_root.name))
    requirements_file = plugin_root.joinpath('requirements.txt')
    if requirements_file.exists():
        # Install required packages using `pip`, with Wheeler Lab wheels server
        # for binary wheels not available on `PyPi`.
        try:
            install(['--find-links', 'http://192.99.4.95/wheels',
                     '--trusted-host', '192.99.4.95', '-r', requirements_file],
                    capture_streams=True)
        except RuntimeError, exception:
            error_message = ('# Error in post-install processing for: %s #' %
                             plugin_root.name)
            hbar = '-' * len(error_message)

            print >> ostream, hbar
            print >> ostream, error_message
            print >> ostream, ''
            print >> ostream, '\n'.join([textwrap.fill(line,
                                                       initial_indent='  ',
                                                       subsequent_indent='  ' *
                                                       2,
                                                       break_on_hyphens=False,
                                                       break_long_words=False)
                                         for line in exception.message
                                         .splitlines()])
            print >> ostream, hbar
            raise SystemExit(-1)
        print >> ostream, ('[%s] Completed post-install processing for: %s' %
                           (str(datetime.now()), plugin_root.name))

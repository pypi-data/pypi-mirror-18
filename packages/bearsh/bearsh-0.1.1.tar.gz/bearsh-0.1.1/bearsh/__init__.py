"""bearsh

Defines ``load_ipython_extension``.
"""

import sys


def load_ipython_extension(shell):
    """
    Run by ``%load_ext bearsh`` in Ipython.

    Registers all availabe bears as IPython magic functions,
    which take a space seperated list of file patterns::

       %PEP8Bear **.py ...

    This
    """
    from coalib.coala import main
    from coalib.collecting.Collectors import get_all_bears_names

    for name in get_all_bears_names():

        def magic(arg_str, _name=name):
            """
            Run a coala bear with give file patterns.
            """
            _argv = list(sys.argv)
            try:
                sys.argv.extend(['-I', '--bears', _name, '--files'] +
                                [','.join(arg_str.split())])
                main()
            finally:
                sys.argv = _argv

        shell.magics_manager.magics['line'][name] = magic

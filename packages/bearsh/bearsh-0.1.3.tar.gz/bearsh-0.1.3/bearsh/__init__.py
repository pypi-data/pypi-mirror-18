"""bearsh

Defines ``load_ipython_extension``.
"""

import sys


def load(shell):
    """
    Called by IPython on ``%load_ext bearsh``.

    Registers all availabe bears as IPython magic functions,
    which take a space seperated list of file patterns::

       %PEP8Bear **.py ...

    This calls :func:`coalib.coala.main` like
    ``coala --bears PEP8Bear --files **.py`` on the command line.
    """
    from coalib.coala import main
    from coalib.collecting.Collectors import get_all_bears_names

    for name in get_all_bears_names():

        def magic(arg_str, _name=name):
            """
            Run a coala bear with give file patterns.
            """
            _argv = list(sys.argv)
            sys.argv[1:] = ['-I', '--bears', _name, '--files',
                            ','.join(arg_str.split())]
            try:
                main()
            finally:
                sys.argv = _argv

        shell.magics_manager.magics['line'][name] = magic


def load_ipython_extension(shell):
    load(shell)

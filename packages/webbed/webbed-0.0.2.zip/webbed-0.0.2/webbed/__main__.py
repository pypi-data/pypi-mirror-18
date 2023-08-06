import sys
from .main import webbed
from .version import __version__

if len(sys.argv) > 1:
    for file in sys.argv[1:]:
        print(webbed(file))
else:
    print(
        """
        Welcome to webbed {}
        Please add the path to a file to execute
        """.format(__version__)
    )
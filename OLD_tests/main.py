import os
import sys

import pytest


# This does NOT work on windows, it just doesn't seem to init the conftest
def main():
    code = pytest.main(
        args=[
            os.path.dirname(os.path.abspath(__file__)),
            *sys.argv[1:],  # pass through any arguments
        ]
    )
    sys.exit(code)


if __name__ == '__main__':
    main()

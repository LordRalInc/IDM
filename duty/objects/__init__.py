try:
    from ._version import __version__  # pyright: ignore
except ImportError:
    import pathlib
    import subprocess

    this_path = pathlib.Path(__file__)
    icad_root = this_path.parent.parent.parent
    out = subprocess.run("git log origin/master-beta -1 --pretty=format:%B",
                         shell=True, cwd=icad_root, capture_output=True).stdout
    out = out.decode('utf-8').splitlines()

    with open(this_path.parent / '_version.py', 'w', encoding='utf-8') as file:
        file.write(f'__version__ = {out[0]!r}')

    __version__ = out[0]


from .events import *
from . import dispatcher as dp
from .database import db

import os
import sys

from pathlib import Path

dir_path = os.path.dirname(os.path.realpath(__file__))
project = str(Path(f'{dir_path}/..').resolve())
site = project + '/website'

sys.path.insert(0, site)
sys.path.insert(0, project + '/env/lib/python3.6/site-packages')
sys.path.insert(0, project + '/env/lib/python3.7/site-packages')
sys.path.insert(0, project + '/env/src/simplerr')
sys.path.insert(0, project)

from manage import create_app  # noqa
from common.loadenv import LoadEnv # noqa

LoadEnv.load_dot_env()
os.environ['PRODUCTION'] = 'true'

# Setup the wsgi application
wsgi = create_app(
    site=site,
    hostname='localhost',
    debugger=False,
    cache=True,
    port=8090
)

application = wsgi.make_app()

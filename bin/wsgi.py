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

from simplerr import dispatcher # noqa
from common.loadenv import LoadEnv # noqa

LoadEnv.load_dot_env()
os.environ['PRODUCTION'] = 'true'

wsgi = dispatcher.wsgi(
    site=site,
    hostname='localhost',
    port=8090,
    threaded=True
)

application = wsgi.make_app()

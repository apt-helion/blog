import os

from pathlib import Path
from dotenv import load_dotenv


class LoadEnv(object):

    _current_path = Path(__file__).parent
    _project_path = _current_path.parent.parent

    @staticmethod
    def load_dot_env():
        if os.environ.get('PRODUCTION'):
            env_path = LoadEnv._project_path / '.env.production'
        else:
            env_path = LoadEnv._project_path / '.env.local'

        load_dotenv(dotenv_path=env_path)

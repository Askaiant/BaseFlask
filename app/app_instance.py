import os
from . import create_app

if os.path.isfile('.ENV'):
    from dotenv import load_dotenv    # noqa
    load_dotenv(verbose=True, dotenv_path='.ENV')

if os.environ.get('FLASK_ENV') == 'production':
    app = create_app('production')
else:
    app = create_app('development')

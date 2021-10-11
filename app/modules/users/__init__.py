from app import api


def init_app(app, **kwargs):
    """
    Init users module.
    """

    # Touch underlying modules
    from . import models, resources, admin, auth    # noqa

    api.add_namespace(resources.api)
    api.add_namespace(auth.api)

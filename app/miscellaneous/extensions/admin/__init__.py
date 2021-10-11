from flask_admin import Admin as BaseAdmin


class Admin(BaseAdmin):

    def __init__(self, app=None, name=None,
                 subdomain=None,
                 translations_path=None,
                 static_url_path=None,
                 base_template=None,
                 template_mode=None,
                 category_icon_classes=None):
        """
        Constructor.

        :param app:
            Flask application object
        :param name:
            Application name. Will be displayed in the main menu and as a page title. Defaults to "Admin"
        :param url:
            Base URL
        :param subdomain:
            Subdomain to use
        :param index_view:
            Home page view to use. Defaults to `AdminIndexView`.
        :param translations_path:
            Location of the translation message catalogs. By default will use the translations
            shipped with Flask-Admin.
        :param endpoint:
            Base endpoint name for index view. If you use multiple instances of the `Admin` class with
            a single Flask application, you have to set a unique endpoint name for each instance.
        :param static_url_path:
            Static URL Path. If provided, this specifies the default path to the static url directory for
            all its views. Can be overridden in view configuration.
        :param base_template:
            Override base HTML template for all static views. Defaults to `admin/base.html`.
        :param template_mode:
            Base template path. Defaults to `bootstrap2`. If you want to use
            Bootstrap 3 or 4 integration, change it to `bootstrap3` or `bootstrap4`.
        :param category_icon_classes:
            A dict of category names as keys and html classes as values to be added to menu category icons.
            Example: {'Favorites': 'glyphicon glyphicon-star'}
        """
        self.app = app

        self.translations_path = translations_path

        self._views = []
        self._menu = []
        self._menu_categories = dict()
        self._menu_links = []

        if name is None:
            name = 'Admin'
        self.name = name

        #self.index_view = index_view or AdminIndexView(endpoint=endpoint, url=url)
        #self.index_view = index_view
        #self.endpoint = endpoint or self.index_view.endpoint
        #self.url = url or self.index_view.url
        self.static_url_path = static_url_path
        self.subdomain = subdomain
        self.base_template = base_template or 'admin/base.html'
        self.template_mode = template_mode or 'bootstrap2'
        self.category_icon_classes = category_icon_classes or dict()

        # Add index view
        #self._set_admin_index_view(index_view=index_view, endpoint=endpoint, url=url)

        # Register with application
        if app is not None:
            self._init_extension()

    def set_index_view(self, index_view=None, endpoint=None, url=None):
        self._set_admin_index_view(index_view=index_view, endpoint=endpoint, url=url)





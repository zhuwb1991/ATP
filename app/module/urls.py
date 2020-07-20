from .views import *

module.add_url_rule('/modules', view_func=ModuleView.as_view('module'))

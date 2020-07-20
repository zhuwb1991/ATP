from .views import *

project.add_url_rule('/projects', view_func=ProjectView.as_view('project'))

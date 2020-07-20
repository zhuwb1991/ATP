from .views import *

interface.add_url_rule('/interface', view_func=InterfaceView.as_view('interface'))

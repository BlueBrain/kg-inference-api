from callbacks.sidebar.on_sidebar_filter_change import on_sidebar_filter_change
from callbacks.sidebar.on_filter_press import on_filter_press
from callbacks.sidebar.on_stored_sidebar_content_update import on_stored_sidebar_content_update


def get_sidebar_callbacks(app):
    on_stored_sidebar_content_update(app)
    on_filter_press(app)
    on_sidebar_filter_change(app)

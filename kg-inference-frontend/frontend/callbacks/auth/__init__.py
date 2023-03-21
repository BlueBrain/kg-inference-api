from callbacks.auth.on_auth_press import on_auth_press
from callbacks.auth.on_stored_token_sidebar_filter import on_stored_token_sidebar_filter
from callbacks.auth.on_token_update import on_token_update


def get_auth_callbacks(app):
    on_auth_press(app)
    on_stored_token_sidebar_filter(app)
    on_token_update(app)

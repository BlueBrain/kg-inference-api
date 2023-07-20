from callbacks.auth import get_auth_callbacks
from callbacks.sidebar import get_sidebar_callbacks
from callbacks.result import get_result_callbacks
from callbacks.rule import get_rule_callbacks


def get_callbacks(app):
    get_auth_callbacks(app)
    get_rule_callbacks(app)
    get_sidebar_callbacks(app)
    get_result_callbacks(app)

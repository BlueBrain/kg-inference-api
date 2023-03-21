from dash import html
from dash_bootstrap_components import Toast
from enum import Enum


class ToastType(Enum):
    SUCCESS = "success"
    WARNING = "warning"
    INFORMATION = "info"
    ERROR = "danger"
    # Not used yet: "light" or "dark", "secondary", "primary"


def make_toast(toast_type: ToastType, message: str):

    title_map = {
        ToastType.INFORMATION: "Information",
        ToastType.WARNING: "Warning",
        ToastType.ERROR: "Error",
        ToastType.SUCCESS: "Success"
    }

    return Toast(
        [html.P(message, className="mb-0")],
        header=title_map[toast_type],
        icon=toast_type.value,
        dismissable=True,
        duration=10000 if toast_type == ToastType.ERROR else 5000
    )


def grey_box(): return html.Div(style={
    "backgroundColor": "var(--bs-card-cap-bg)",
    "minHeight": "300px",
    "height": "100%"
})

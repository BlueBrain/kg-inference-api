import argparse
from dash import Dash
from layout.layout import page
from callbacks import get_callbacks

external_stylesheets = [
    {
        'rel': 'stylesheet',
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css",
        "integrity": "sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65",
        "crossorigin": "anonymous"
    }
]

external_scripts = [
    {
        "src": "https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js",
        "integrity": "sha384-oBqDVmMz9ATKxIep9tiCxS/Z9fNfEXiDAYTujMAeBAsjFuCZSmKbSSUnQlmh/jp3",
        "crossorigin": "anonymous"
    },
    {
        "src": "https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js",
        "integrity": "sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4",
        "crossorigin": "anonymous"
    }
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    suppress_callback_exceptions=True,
    title="KG Inference Rules",
)

app.layout = page
get_callbacks(app)

server = app.server


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    app.run_server(debug=args.debug)

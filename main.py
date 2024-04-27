try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
except Exception:
    raise

from dash import Dash
from src import DASH_ASSETS, layout


PROJECT = "Simple Rich Trading Protocol"


def run():
    app = Dash(
        PROJECT,
        title=PROJECT,
        update_title="working...",
        assets_folder=DASH_ASSETS
    )
    app.layout = layout.LAYOUT

    try:
        from src import callbacks
    except Exception:
        raise
    app.run(debug=False)


if __name__ == "__main__":
    run()

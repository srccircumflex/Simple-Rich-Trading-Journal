try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent))
except Exception:
    raise

from __version__ import __project_name__

from dash import Dash
from src import DASH_ASSETS, layout


def run():
    app = Dash(
        __project_name__,
        title=__project_name__,
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

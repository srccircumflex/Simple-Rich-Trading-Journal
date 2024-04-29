try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
except Exception:
    raise

import demo
import main

if __name__ == "__main__":
    demo.init(demo.ID)
    main.__project_name__ = f"(demo){demo.ID} {main.__project_name__}"
    main.run()

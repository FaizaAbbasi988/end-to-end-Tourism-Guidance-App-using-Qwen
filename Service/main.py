"""Run the Tourism AI service with `python Service/main.py` or `python -m Service.main`."""
import sys
from pathlib import Path

import uvicorn

# When run as a script, Python adds Service/ instead of the repo root to
# sys.path. Add the root once; `python -m Service.main` requires no adjustment.
if __package__ in (None, ""):
    repository_root = str(Path(__file__).resolve().parent.parent)
    if repository_root not in sys.path:
        sys.path.insert(0, repository_root)

from Service.app import create_app, register_router

app = create_app()
register_router(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

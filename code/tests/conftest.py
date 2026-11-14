import sys
import shutil
from pathlib import Path

import pytest


llm_root = Path(__file__).parents[1]
if str(llm_root) not in sys.path:
    sys.path.insert(0, str(llm_root))


@pytest.fixture
def tmp_path(request):
    """Workspace-local replacement for inaccessible Windows sandbox TEMP."""
    root = Path(__file__).parent / ".tmp" / request.node.name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    yield root
    if root.exists():
        shutil.rmtree(root)

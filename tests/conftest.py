import pytest


@pytest.fixture
async def spaeti(lona_project_context, transactional_db):
    import os

    import spaeti

    context = await lona_project_context(
        project_root=os.path.dirname(spaeti.__file__),
        settings=['settings.py'],
    )

    yield context

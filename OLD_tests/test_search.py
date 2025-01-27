import pytest

from shade import ShadeLocal
from shade.v1.models import AssetModel, Job
from tests.helpers import wait_for_jobs


@pytest.mark.parametrize(
    'demo_file_name',
    ['text/README.md', 'text/semestesr-1-2023-24.pdf', 'text/semestesr-1-2023-24.pdf'],
)
def test_text_in_search(
    demo_asset: AssetModel,
    backend: ShadeLocal,
):
    backend.models.enable_model('text')

    asset = wait_for_jobs(backend, [Job.METADATA, Job.TEXT], [demo_asset])[0]

    result = backend.search.search()

    assert any(asset.id == a.id for a in result)


@pytest.mark.parametrize(
    'demo_file_name', ['audio/Cymatics - Buildup Drums 19 - 140 BPM.wav']
)
def test_audio_in_search(
    demo_asset: AssetModel,
    backend: ShadeLocal,
):
    # Fixes the issue of audio not returned on search
    backend.models.enable_model('audio')

    asset = wait_for_jobs(backend, [Job.METADATA, Job.AUDIO], [demo_asset])[0]

    result = backend.search.search()

    assert any(asset.id == a.id for a in result)

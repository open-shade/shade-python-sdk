import os
import subprocess
from pathlib import Path
from typing import List
import pytest
from google.cloud import storage

from shade import ShadeLocal


@pytest.fixture(scope="session")
def backend() -> ShadeLocal:
    backend = ShadeLocal(port=int(os.getenv('SHADE_PORT', 9082)))
    assert backend.server.status() == 'online'

    # backend.models.enable_all_models()
    backend.models.enable_model('blip')
    backend.models.enable_model('audio')
    backend.models.enable_model('text')
    backend.models.enable_model('braw')

    return backend


@pytest.fixture(scope="session")
def test_assets(pytestconfig) -> Path:
    data_dir = pytestconfig.cache.mkdir('test_assets')
    print('Synchronizing test assets from GCS (this may take a while)...')
    res = subprocess.run([
        'gsutil',
        'rsync',
        '-r', '-d',
        'gs://shade-test-assets/',
        str(data_dir.resolve())
    ])
    if res.returncode != 0:
        pytest.skip('Failed to download demo assets. Running test suite without them.')

    return data_dir.resolve()


@pytest.fixture
def demo_file_paths(pytestconfig, demo_file_names: List[str], tmp_path) -> List[Path]:
    """
    Fixture to request a bunch of paths for a test.

    :param demo_file_names: name of the asset.
    """
    cache_dir = pytestconfig.cache.mkdir("demo_assets")

    demo_file_paths = []
    for demo_file_name in demo_file_names:
        asset_path = cache_dir / demo_file_name
        # TODO check for changes in the remote asset
        if not asset_path.exists():
            print(
                f"downloading demo asset {demo_file_name} because it was not found in the cache"
            )
            storage_client = storage.Client.create_anonymous_client()
            bucket = storage_client.bucket("shade-test-assets")
            blob = bucket.blob(demo_file_name)
            asset_path.parent.mkdir(parents=True, exist_ok=True)
            blob.download_to_filename(str(asset_path))

        # copy it somewhere safe, in case the test modifies it
        # we could use tempfile here but i'm lazy
        tmp_asset_path = tmp_path / demo_file_name
        tmp_asset_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_asset_path.write_bytes(asset_path.read_bytes())

        demo_file_paths.append(tmp_asset_path)

    yield demo_file_paths

    for tmp_asset_path in demo_file_paths:
        tmp_asset_path.unlink(missing_ok=True)

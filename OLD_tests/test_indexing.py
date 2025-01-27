"""
This test suite assumes that a shade server is running on the same computer as the tests so that everything stays
referenced
"""

import platform

import pytest

from shade import ShadeLocal
from shade.v1.models import AssetModel, Job, JobState
from tests.helpers import wait_for_jobs


@pytest.mark.parametrize(
    'demo_file_names',
    [
        [
            'video/coverr-berlin-underground-train-7268-original.mp4',
            # TODO doesn't seem like braw is working
            'video/braw-r3d/A002_C305_0523UB_001.R3D',
            'video/Filmplusgear-skiers-Samnaun-2019-dci-Q5.braw'
            if platform.system() != 'Linux'
            else None,
            'image/exr-hdr-weird/bw_full.exr',
            'image/exr-hdr-weird/bw_half.exr',
            'image/exr-hdr-weird/rgb_full.exr',
            'image/exr-hdr-weird/rgb_half.exr',
            'image/exr-hdr-weird/rgba_full.exr',
            'image/exr-hdr-weird/rgba_half.exr',
            'image/DSC01974.ARW',
            'image/DSC04274.ARW',
            'image/FullSizeRender.heic',
            'image/android.demo-popover.gif',
            'image/photo-1.jpg',
            'image/photo-2.jpg',
            'image/photo-3.jpg',
            'image/schema.webp',
            # exr's are failing on my machine -matias
            'image/exr-hdr-weird/farm_sunset_1k.hdr',
            'image/exr-hdr-weird/limpopo_golf_course_1k.hdr',
            'image/exr-hdr-weird/sample_640426.hdr',
            'photoshop/model_157142297.psd',
            'illustrator/example.ai',
        ]
    ],
)
def test_visual_assets_batched(
    demo_assets: list[AssetModel],
    backend: ShadeLocal,
):
    # wait for jobs to run
    for asset in wait_for_jobs(
        backend, [Job.METADATA, Job.CORE, Job.PREVIEWS, Job.COLOR_PALETTE], demo_assets
    ):
        assert asset.signature
        assert asset.ai_indexed
        assert asset.palette
        assert asset.preview_images
        assert asset.tags


@pytest.mark.parametrize(
    'demo_file_name',
    [
        'audio/Cymatics - Buildup Drums 19 - 140 BPM.wav',
        'audio/Cymatics - Buildup Drums 20 - 140 BPM.wav',
        'audio/Cymatics - Buildup Drums 24 - 150 BPM.wav',
        'audio/Snap Sound Effect [ HD ].mp3',
        'audio/item_purchase.ogg',
    ],
)
def test_audio_assets(
    demo_asset: AssetModel,
    backend: ShadeLocal,
):
    backend.models.enable_model('audio')
    asset = wait_for_jobs(backend, [Job.METADATA, Job.AUDIO], [demo_asset])[0]

    # assert asset.size_bytes
    assert asset.tags
    assert asset.ai_indexed


@pytest.mark.parametrize(
    'demo_file_name',
    ['text/README.md', 'text/semestesr-1-2023-24.pdf', 'text/semestesr-1-2023-24.pdf'],
)
def test_text_assets(
    demo_asset: AssetModel,
    backend: ShadeLocal,
):
    backend.models.enable_model('text')

    asset = wait_for_jobs(backend, [Job.METADATA, Job.TEXT], [demo_asset])[0]

    assert asset.ai_indexed


@pytest.mark.parametrize(
    'demo_file_names',
    [
        [f'images/freeman{i}.jpg' for i in range(1, 8)],
    ],
)
def test_facial_recognition_batched(
    demo_assets: list[AssetModel],
    backend: ShadeLocal,
):
    backend.models.enable_model('facial')

    assets = wait_for_jobs(
        backend, [Job.METADATA, Job.FACIAL_RECOGNITION, Job.CORE], demo_assets
    )

    # TODO check for individuals

    for asset in assets:
        assert asset.facial_recognition_job_state == JobState.COMPLETED
        # TODO query/check faces
        # assert backend.assets.get_faces(asset.id)

import pytest
from PIL import Image

from shade import ShadeLocal


@pytest.mark.parametrize(
    'demo_file_name',
    [
        'image/DSC01974.ARW',
        'image/photo-3.jpg',
        'image/exr-hdr-weird/rgba_half.exr',
    ],
)
def test_ocio(demo_file_path, backend: ShadeLocal, tmp_path):
    assert isinstance(
        backend.convert.convert_colorspace(demo_file_path, 'sRGB - Texture', 'ACEScg'),
        Image.Image,
    )

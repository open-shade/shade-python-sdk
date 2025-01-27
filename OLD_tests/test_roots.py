from pathlib import Path

from shade import ShadeLocal


def test_add_remove_root(backend: ShadeLocal, tmp_path: str):
    tmp_path = Path(tmp_path)

    root_id = backend.roots.add_new_root(tmp_path)

    assert root_id
    assert root_id in [root.id for root in backend.roots.get_roots()]

    backend.roots.delete_root(root_id)
    assert root_id not in [root.id for root in backend.roots.get_roots()]

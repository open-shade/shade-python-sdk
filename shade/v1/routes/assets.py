# TODO Lookup asset by path, get all assets, get an asset by id, update an asset's attributes
#  rename maybe?
import uuid

from shade.v1.api import API
from shade.v1.types import MountInfo
from shade.v1.models import AssetModel
from pathlib import Path
from typing import List


class Assets:
    def __init__(self, api: API, mount_info: MountInfo):
        self.__api = api
        self.__mount_info = mount_info

    def get_all_assets(self) -> List[AssetModel]:
        assets = self.__api.get('assets')

        return [AssetModel(**asset) for asset in assets.json()]

    def get_asset_by_id(self, id_: uuid.UUID) -> AssetModel:
        asset = self.__api.get(f'assets/{id_}')

        return AssetModel(**asset.json())

    def get_asset_by_path(self, path: Path) -> AssetModel:
        """
        TODO handle translation (or not)
        Get an asset by its path

        :param path: The path to the asset
        :return: The asset
        """
        asset = self.__api.get(f'indexing/file', params={
            'path': str(path)
        })

        return AssetModel(**asset.json())

    def update_asset(self,
                     id_: uuid.UUID,
                     description: str = None,
                     rating: int = None,
                     category: str = None,
                     tags: list = None,) -> None:
        """
        Update an asset's attributes
        :param id_: The id of the asset to update
        :param description: The new description
        :param rating: The new rating (0-5)
        :param category: The new category
        :param tags: The new tags - this overrides the existing tags
        :return:
        """
        self.__api.put(f'assets/{id_}', json={
            'description': description,
            'rating': rating,
            'category': category,
            'tags': tags
        })

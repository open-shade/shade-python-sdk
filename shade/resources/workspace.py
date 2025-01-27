from typing import Optional
from uuid import UUID

import requests

from .abc_resource import ABCResource


class Workspace(ABCResource):
    def get_workspaces(self) -> dict:
        resp = requests.get(
            self.auth.remote_url + '/workspaces',
            headers={'Authorization': self.auth.api_key},
        )
        resp.raise_for_status()
        return resp.json()

    def get_workspace_by_id(self, id_: UUID) -> dict:
        """
        Return the workspace with the given id
        :param id_: The id of the workspace
        :return: The workspace
        """
        resp = requests.get(
            self.auth.remote_url + f'/workspaces/{id_}',
            headers={'Authorization': self.auth.api_key},
        )
        resp.raise_for_status()
        return resp.json()

    def get_workspace_by_domain(self, domain: str) -> dict:
        """
        Return the first matching workspace to the given name
        :param name: The domain of the workspace
        :return: The workspace
        """
        workspaces = self.get_workspaces()

        for workspace in workspaces:
            if workspace['domain'] == domain:
                return workspace

        raise ValueError(f'No workspace with domain {domain}')

    def get_workspace_by_name(self, name: str) -> dict:
        """
        Return the first matching workspace to the given name
        :param name: The name of the workspace
        :return: The workspace
        """
        workspaces = self.get_workspaces()

        for workspace in workspaces:
            if workspace['name'] == name:
                return workspace

        raise ValueError(f'No workspace with name {name}')

    def create_workspace(
        self,
        name: str,
        domain: str,
        description: Optional[str] = None,
        thumbnail: Optional[str] = None,
    ) -> dict:
        """
        Create a new workspace
        :param name: The name of the workspace
        :param domain: The domain for the workspace
        :param description: The description for the workspace
        :param thumbnail: The thumbnail for the workspace
        :return: The created workspace details
        """
        payload = {
            'name': name,
            'description': description,
            'thumbnail': thumbnail,
            'domain': domain,
            'team_size_analytics': '1-10',
            'team_usage_analytics': 'team',
        }

        resp = requests.post(
            self.auth.remote_url + '/workspaces',
            headers={'Authorization': self.auth.api_key},
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()

    def delete_workspace(self, id_: UUID) -> dict:
        """
        Delete the workspace with the given id
        :param id_: The id of the workspace
        :return: The deleted workspace
        """
        resp = requests.delete(
            self.auth.remote_url + f'/workspaces/{id_}',
            headers={'Authorization': self.auth.api_key},
        )
        resp.raise_for_status()
        return resp.json()

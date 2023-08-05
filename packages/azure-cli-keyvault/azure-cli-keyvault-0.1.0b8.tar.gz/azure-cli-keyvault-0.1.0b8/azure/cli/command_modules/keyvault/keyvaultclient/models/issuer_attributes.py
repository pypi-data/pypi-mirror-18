#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------
# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------
#pylint: skip-file
from msrest.serialization import Model


class IssuerAttributes(Model):
    """The attributes of an issuer managed by the KeyVault service.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param enabled: Determines whether the issuer is enabled
    :type enabled: bool
    :ivar created: Creation time in UTC
    :vartype created: datetime
    :ivar updated: Last updated time in UTC
    :vartype updated: datetime
    """ 

    _validation = {
        'created': {'readonly': True},
        'updated': {'readonly': True},
    }

    _attribute_map = {
        'enabled': {'key': 'enabled', 'type': 'bool'},
        'created': {'key': 'created', 'type': 'unix-time'},
        'updated': {'key': 'updated', 'type': 'unix-time'},
    }

    def __init__(self, enabled=None):
        self.enabled = enabled
        self.created = None
        self.updated = None

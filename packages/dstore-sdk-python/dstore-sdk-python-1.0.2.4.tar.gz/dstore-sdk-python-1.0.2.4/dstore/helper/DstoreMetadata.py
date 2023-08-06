#!/usr/bin/env python
# -*- coding: utf-8 -*-
class DstoreMetadata:
    """
    Convinience class to deal with different kind of metadata provided by the dstoreIO grpc server.
    """

    ENGINE_RETURN_STATUS_KEY = 'dstore-engine-returnstatus'
    USERNAME_KEY = 'dstore-username'
    PASSWORD_KEY = 'dstore-password'
    ACCESS_TOKEN_KEY = 'dstore-accesstoken'

    @staticmethod
    def buildTrailingMetadata(metadata):
        """
        Convert the list of tuples metadata to a dict {'metadata_key': value} for easier access.

        :param list metadata: list of tuples containing ('metadata_key', value)
        :return: dict metadata
        """
        metadata_dict = {}
        for current_metadata in metadata:
            metadata_dict[current_metadata[0]] = current_metadata[1]
        return metadata_dict
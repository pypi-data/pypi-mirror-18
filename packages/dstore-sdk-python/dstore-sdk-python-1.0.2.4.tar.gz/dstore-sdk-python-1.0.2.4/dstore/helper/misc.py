#!/usr/bin/env python
# -*- coding: utf-8 -*-
import grpc
from DstoreMetadata import DstoreMetadata

def getChannel(server, port, pem_file_path, username=None, password=None, accesstoken='default'):
    """
    Get a channel object.

    :param str server: grpc server
    :param int port: grpc server port
    :param str pem_file_path: path to pem file
    :param str username: grpc username
    :param str password: grpc password
    :param str accesstoken: grpc accesstoken
    :return: channel
    """
    # Build channel credentials. If file is not present, throw error.
    with open(pem_file_path, 'r') as myfile:
        pem_data = myfile.read()
    channel_cerdentials = grpc.ssl_channel_credentials(pem_data)
    # Now also build call credentials. These will add the authtokens as metadata to each call.
    if username is not None and password is not None:
        call_credentials = grpc.metadata_call_credentials(lambda context, callback: callback([(DstoreMetadata.USERNAME_KEY, username),
                                                                                              (DstoreMetadata.PASSWORD_KEY, password),
                                                                                              (DstoreMetadata.ACCESS_TOKEN_KEY, accesstoken)], None),
                                                          name='dstoreio_credentials')
        # Merge both credentials.
        channel_cerdentials = grpc.composite_channel_credentials(channel_cerdentials, call_credentials)

    channel = grpc.secure_channel('%s:%s' % (server, port), channel_cerdentials)
    return channel

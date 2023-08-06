#!/usr/bin/env python
# -*- coding: utf-8 -*-
import grpc

def getChannel(server, port, pem_file_path, username=None, password=None, accesstoken='default'):
    # Build channel credentials. If file is not present, throw error.
    with open(pem_file_path, 'r') as myfile:
        pem_data = myfile.read()
    channel_cerdentials = grpc.ssl_channel_credentials(pem_data)
    # Now also build call credentials. These will add the authtokens as metadata to each call.
    if username is not None and password is not None:
        call_credentials = grpc.metadata_call_credentials(lambda context, callback: callback([('dstore-username', username),
                                                                                              ('dstore-password', password),
                                                                                              ('dstore-accesstoken', accesstoken)], None),
                                                          name='dstoreio_credentials')
        # Merge both credentials.
        channel_cerdentials = grpc.composite_channel_credentials(channel_cerdentials, call_credentials)

    channel = grpc.secure_channel('%s:%s' % (server, port), channel_cerdentials)
    return channel

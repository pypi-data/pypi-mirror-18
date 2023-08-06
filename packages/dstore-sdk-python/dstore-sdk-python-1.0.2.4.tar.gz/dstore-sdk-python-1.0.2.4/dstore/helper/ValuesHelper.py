#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
import time
import dstore.values_pb2
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp as ProtobufTimestamp

ORIG_TYPES_TO_CONV_TYPE = { type(None): 'ProtobufNone',
                            type(False): 'ProtobufBoolean',
                            type(1): 'ProtobufInteger',
                            type(0.1): 'ProtobufFloat',
                            type(''): 'ProtobufString',
                            type(u''): 'ProtobufUnicode',
                            type(()): 'ProtobufTuple',
                            type([]): 'ProtobufList',
                            type({}): 'ProtobufDictionary',
                            type(ProtobufTimestamp()): 'NativeTimestamp'}

class ValuesHelper(object):
    """
    Convinience class to convert a native python value to a grpc value or vice versa.
    """

    logger = logging.getLogger('ValuesHelper')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename=None,
                        filemode='w')

    @staticmethod
    def buildValue(value_content):
        """
        This method tries to guess the target value type by the source value type, using the ORIG_TYPES_TO_CONV_TYPE
        mapping.

        :param value_content
        :return: converted_value
        """
        value_type = type(value_content)
        try:
            return getattr(ValuesHelper, "build%sValue" % ORIG_TYPES_TO_CONV_TYPE[value_type])(value_content)
        except KeyError:
            etype, evalue, etb = sys.exc_info()
            ValuesHelper.logger.error("Unkown value type: %s. Exception: %s, Error: %s" % (value_type, etype, evalue))
            sys.exit(255)
        except AttributeError:
            etype, evalue, etb = sys.exc_info()
            ValuesHelper.logger.error("No method build%sValue exists. Exception: %s, Error: %s" % (ORIG_TYPES_TO_CONV_TYPE[value_type], etype, evalue))
            sys.exit(255)

    @staticmethod
    def buildProtobufIntegerValue(value_content):
        int_value = dstore.values_pb2.integerValue()
        int_value.value = value_content
        return int_value

    @staticmethod
    def buildProtobufStringValue(value_content):
        string_value = dstore.values_pb2.stringValue()
        string_value.value = value_content
        return string_value

    @staticmethod
    def buildProtobufBytesValue(value_content):
        bytes_value = dstore.values_pb2.bytesValue()
        bytes_value.value = value_content
        return bytes_value

    @staticmethod
    def buildProtobufDoubleValue(value_content):
        double_value = dstore.values_pb2.doubleValue()
        double_value.value = value_content
        return double_value

    @staticmethod
    def buildProtobufBooleanValue(value_content):
        bool_value = dstore.values_pb2.booleanValue()
        bool_value.value = value_content
        return bool_value

    @staticmethod
    def buildProtobufDecimalValue(value_content):
        decimal_value = dstore.values_pb2.decimalValue()
        decimal_value.value = value_content
        return decimal_value

    @staticmethod
    def buildProtobufTimestampValue(value_content):
        timestamp_value = dstore.values_pb2.timestampValue()
        timestamp_value.value = value_content
        return timestamp_value

    @staticmethod
    def buildProtobufLongValue(value_content):
        long_value = dstore.values_pb2.longValue()
        long_value.value = value_content
        return long_value

    @staticmethod
    def buildNativeTimestampValue(value_content):
        datetime_obj = datetime.utcfromtimestamp(float('%s.%s' % (value_content.seconds, value_content.nanos)))
        timestamp_value = time.mktime(datetime_obj.timetuple())
        return timestamp_value

    @staticmethod
    def buildNativeDatetimeValue(value_content):
        datetime_obj = datetime.utcfromtimestamp(float('%s.%s' % (value_content.seconds, value_content.nanos)))
        return datetime_obj

    @staticmethod
    def buildNativeDecimalValue(value_content):
        decimal_value = float(value_content)
        return decimal_value
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
import dstore.values_pb2

TYPES_TO_TYPENAMES= {type(None): 'None',
                     type(False): 'Boolean',
                     type(1): 'Integer',
                     type(0.1): 'Float',
                     type(''): 'String',
                     type(u''): 'Unicode',
                     type(()): 'Tuple',
                     type([]): 'List',
                     type({}): 'Dictionary'}

class ValuesHelper(object):

    logger = logging.getLogger('ValuesHelper')
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename=None,
                        filemode='w')

    @staticmethod
    def buildValue(value_content):
        value_type = type(value_content)
        try:
            return getattr(ValuesHelper, "build%sValue" % TYPES_TO_TYPENAMES[value_type])(value_content)
        except KeyError:
            etype, evalue, etb = sys.exc_info()
            ValuesHelper.logger.error("Unkown value type: %s. Exception: %s, Error: %s" % (value_type, etype, evalue))
            sys.exit(255)
        except AttributeError:
            etype, evalue, etb = sys.exc_info()
            ValuesHelper.logger.error("No method %s exists. Exception: %s, Error: %s" % (value_type, etype, evalue))
            sys.exit(255)

    @staticmethod
    def buildIntegerValue(value_content):
        int_value = dstore.values_pb2.integerValue()
        int_value.value = value_content
        return int_value

    @staticmethod
    def buildStringValue(value_content):
        string_value = dstore.values_pb2.stringValue()
        string_value.value = value_content
        return string_value

    @staticmethod
    def buildBytesValue(value_content):
        bytes_value = dstore.values_pb2.bytesValue()
        bytes_value.value = value_content
        return bytes_value

    @staticmethod
    def buildDoubleValue(value_content):
        double_value = dstore.values_pb2.doubleValue()
        double_value.value = value_content
        return double_value

    @staticmethod
    def buildBooleanValue(value_content):
        bool_value = dstore.values_pb2.booleanValue()
        bool_value.value = value_content
        return bool_value

    @staticmethod
    def buildDecimalValue(value_content):
        decimal_value = dstore.values_pb2.decimalValue()
        decimal_value.value = value_content
        return decimal_value

    @staticmethod
    def buildTimestampValue(value_content):
        timestamp_value = dstore.values_pb2.timestampValue()
        timestamp_value.value = value_content
        return timestamp_value

    @staticmethod
    def buildLongValue(value_content):
        long_value = dstore.values_pb2.longValue()
        long_value.value = value_content
        return long_value

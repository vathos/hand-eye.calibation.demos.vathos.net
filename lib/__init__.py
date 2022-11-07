# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2017, Vathos GmbH
#
# All rights reserved.
#
###############################################################################

import logging
import os

root_logger = logging.getLogger(None)
root_logger.handlers = []
logging.basicConfig(
    format=
    '%(asctime)s,%(msecs)d %(levelname)-2s ' \
    '[%(filename)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d:%H:%M:%S',
    level=os.environ.get('LOG_LEVEL', 'INFO'))

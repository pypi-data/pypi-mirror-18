# Copyright 2016 DataStax, Inc.
#
# Licensed under the DataStax DSE Driver License;
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at
#
# http://www.datastax.com/terms/datastax-dse-driver-license-terms

import logging
import os


class NullHandler(logging.Handler):
    def emit(self, record):
            pass

logging.getLogger('dse').addHandler(NullHandler())

__version_info__ = (1, 1, 0)
__version__ = '.'.join(map(str, __version_info__))

_core_driver_target_version = '3.7.1'
_use_any_core_driver_version = bool(os.environ.get('DSE_DRIVER_PERMIT_UNSUPPORTED_CORE'))

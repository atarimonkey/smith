#!/usr/bin/env python2
#
# This is to test the log.py functionality.

import log


test_logger = log.Log("log_test")

test_logger.logger.info('This is a test.')
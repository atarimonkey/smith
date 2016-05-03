#!/usr/bin/env python2
#
# This is to test the log.py functionality.

import log


test_logger = log.Log("log_test")

test_logger.log_to_file('This is a test.')
test_logger.log_to_web(1, 2, 3, 4, 5, 6, 7, 8)
test_logger.log_to_all(10, 11, 12, 13, 14, 15, 16, 17)